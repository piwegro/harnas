# Flask import
from flask import Flask, request, make_response
from flask_cors import CORS

# Exceptions import
from exc import PostgresError, FirebaseError, \
    UserNotFoundError, UserAlreadyExistsError, CurrencyNotFoundError, OfferNotFoundError


# Functions and classes import
from currencies import Currency
from error import Error
from firebase import FirebaseUser, initialize_firebase
from health import check_health
from images import Image
from messages import Message
from offers import Offer
from users import User

from json_encoder import APIEncoder, as_json

app = Flask(__name__)
app.json_encoder = APIEncoder

CORS(app)

initialize_firebase()


# GETTING OFFERS
# Get a single offer by  its id
@as_json
@app.route("/offer/<offer_id>", methods=["GET"])
def hande_get_offer_by_id(offer_id: str):
    try:
        return Offer.get_offer_by_id(offer_id), 200
    except OfferNotFoundError:
        return Error("Offer not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Get all offers for a query (paginated)
@as_json
@app.route("/offers/search/<query>/<page>", methods=["GET"])
def handle_get_offers_by_query(query: str, page: int):
    try:
        resp = make_response(Offer.search_offers(query, page))
        resp.status_code = 200
        # TODO: Set the correct headers
        # resp.headers["X-Total-Count"] = 0
        return resp
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Get all offers (paginated)
@as_json
@app.route("/offers/<page>", methods=["GET"])
def handle_get_all_offers(page: int):
    try:
        resp = make_response(Offer.get_all_offers())
        resp.status_code = 200
        # TODO: Set the correct headers
        # resp.headers["X-Total-Count"] = 0
        return resp
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Get all offers by a user id (not paginated)
@as_json
@app.route("/user/<user_id>/offers", methods=["GET"])
def handle_get_offers_by_user_id(user_id: str):
    try:
        return Offer.get_offers_by_user_id(user_id), 200
    except UserNotFoundError:
        return Error("User not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# ADDING OFFERS
# Add a single offer
@as_json
@app.route("/offer", methods=["POST"])
def handle_add_offer():
    # TODO: Handle images

    data = request.get_json()

    try:
        title = data["title"]
    except KeyError:
        return Error("Missing field: 'title'"), 400

    try:
        description = data["description"]
    except KeyError:
        return Error("Missing field: 'description'"), 400

    try:
        currency_symbol = data["currency"]
    except KeyError:
        return Error("Missing field: 'currency'"), 400

    try:
        price = data["price"]
    except KeyError:
        return Error("Missing field: 'price'"), 400

    try:
        location = data["location"]
    except KeyError:
        return Error("Missing field: 'location'"), 400

    try:
        images = data["images"]
    except KeyError:
        return Error("Missing field: 'images'"), 400

    try:
        seller_id = data["seller_id"]
    except KeyError:
        return Error("Missing field: 'seller_id'"), 400

    try:
        price = int(price)
    except ValueError:
        return Error("Invalid price"), 400

    try:
        # TODO: Remove after implementing handling images
        images = Image.dummies()
        offer = Offer.new_offer_with_id(title, description, currency_symbol, price, seller_id, images, location)
    except UserNotFoundError:
        return Error("User not found"), 400
    except CurrencyNotFoundError:
        return Error("Currency not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500

    try:
        offer.add()
    except PostgresError as e:
        print("PostgresError:", e)
        return Error("Internal server error"), 500

    return offer, 201


# Post images
@as_json
@app.route("/images", methods=["POST"])
def handle_post_images():
    try:
        return Image.dummies(), 201
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# USER MANAGEMENT
# Get a single user's info (including accepted currencies) by its id
@app.route("/user/<user_id>", methods=["GET"])
@as_json
def handle_user_by_id(user_id: str):
    try:
        return User.get_user_by_id(user_id), 200
    except UserNotFoundError:
        return Error("User not found"), 404


# Put a new user in the database (after sign up)
@app.route("/user/<user_id>", methods=["PUT"])
@as_json
def handle_add_user_to_db(user_id: str):
    try:
        fuser = FirebaseUser.get_user_by_uid(user_id)
    except UserNotFoundError:
        return Error("User not found"), 400
    except FirebaseError as e:
        print("FirebaseError:", e)
        return Error("Internal error"), 500

    try:
        user = User.from_firebase_user(fuser)
    except UserAlreadyExistsError:
        return Error("User already exists"), 409
    except PostgresError as e:
        print("FirebaseError:", e)
        return Error("Internal server error"), 500

    return user, 201


# Update a single user's info (including accepted currencies)
@as_json
@app.route("/user/<user_id>", methods=["PATCH"])
def handle_update_user(user_id: str):
    return None, 204


# MESSAGES
# Get all messages from and to a user
@as_json
@app.route("/user/<user_id>/conversations", methods=["GET"])
def handle_get_user_conversations(user_id: str):
    try:
        result = Message.get_messages_by_user_id(user_id)
        return result, 200
    except UserNotFoundError:
        return Error("User with given ID not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Send a single new message to another user
@as_json
@app.route("/message", methods=["POST"])
def handle_send_message():
    data = request.get_json()

    try:
        sender_id = data["sender_id"]
    except KeyError:
        return Error("Missing field: sender_id"), 400

    try:
        receiver_id = data["receiver_id"]
    except KeyError:
        return Error("Missing field: receiver_id"), 400

    try:
        content = data["content"]
    except KeyError:
        return Error("Missing field: content"), 400

    try:
        m = Message.new_message_with_ids(sender_id, receiver_id, content)
        m.send()
    except UserNotFoundError:
        return Error("At least one of the users not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500

    return m, 201


# CURRENCIES
# Get all currencies accepted by the system
@as_json
@app.route("/currencies", methods=["GET"])
def handle_get_all_currencies():
    try:
        return Currency.get_currencies(), 200
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# MISCELLANEOUS
# Check the server's status
@as_json
@app.route("/health", methods=["GET"])
def handle_health():
    status, message = check_health()
    status_code = 200 if status else 503
    return {
        "healthy": status,
        "message": message
    }, status_code


# Handle root queries
@app.route("/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def handle_root():
    return "You've reached the root of the internal Piwegro API. Unfortunately, there's nothing here."
