# Flask import
from flask import Flask, request

# Exceptions import
from exc import UserNotFoundError, CurrencyNotFoundError, PostgresError, FirebaseError, UserAlreadyExistsError, \
    OfferNotFoundError

# Functions and classes import
from currencies import Currency
from error import Error
from firebase import FirebaseUser, initialize_firebase
from health import check_health
from messages import Message
from offers import Offer
from users import User


app = Flask(__name__)
initialize_firebase()


# GETTING OFFERS
# Get a single offer by  its id
@app.route("/offer/<offer_id>", methods=["GET"])
def hande_get_offer_by_id(offer_id: str):
    try:
        offer = Offer.get_offer_by_id(offer_id)
    except OfferNotFoundError:
        return Error("Offer not found").to_json(400)
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)

    return vars(offer)


# Get all offers for a query (paginated)
@app.route("/offers/search/<query>/<page>", methods=["GET"])
def handle_get_offers_by_query(query: str, page: str):
    return "", 204


# Get all offers (paginated)
@app.route("/offers/<page>", methods=["GET"])
def handle_get_all_offers(page: int):
    try:
        offers = Offer.get_all_offers()
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)

    return offers


# Get all offers by a user id (not paginated)
@app.route("/user/<user_id>/offers", methods=["GET"])
def handle_get_offers_by_user_id(user_id: str):
    try:
        offers = Offer.get_offers_by_user_id(user_id)
    except UserNotFoundError:
        return Error("User not found").to_json(400)
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)

    return offers


# ADDING OFFERS
# Add a single offer
@app.route("/offer", methods=["POST"])
def handle_add_offer():
    # TODO: Handle images

    data = request.get_json()

    try:
        title = data["title"]
    except KeyError:
        return Error("Missing field: 'title'").to_json(400)

    try:
        description = data["description"]
    except KeyError:
        return Error("Missing field: 'description'").to_json(400)

    try:
        currency_symbol = data["currency"]
    except KeyError:
        return Error("Missing field: 'currency'").to_json(400)

    try:
        price = data["price"]
    except KeyError:
        return Error("Missing field: 'price'").to_json(400)

    try:
        location = data["location"]
    except KeyError:
        return Error("Missing field: 'location'").to_json(400)

    try:
        images = data["images"]
    except KeyError:
        return Error("Missing field: 'images'").to_json(400)

    try:
        seller_id = data["seller_id"]
    except KeyError:
        return Error("Missing field: 'seller_id'").to_json(400)

    try:
        offer = Offer.new_offer_with_id(title, description, currency_symbol, price, seller_id, [])
    except UserNotFoundError:
        return Error("User not found").to_json(400)
    except CurrencyNotFoundError:
        return Error("Currency not found").to_json(400)
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)

    try:
        offer.add()
    except PostgresError as e:
        print("PostgresError:", e)
        return Error("Internal server error").to_json(500)

    return vars(offer)


# Post images
@app.route("/images", methods=["POST"])
def handle_post_images():
    return "", 204


# USER MANAGEMENT
# Get a single user's info (including accepted currencies) by its id
@app.route("/user/<user_id>", methods=["GET"])
def handle_user_by_id(user_id: str):
    try:
        user = User.get_user_by_id(user_id)
    except UserNotFoundError:
        return Error("User not found").to_json(404)

    return vars(user), 200


# Put a new user in the database (after sign up)
@app.route("/user/<user_id>", methods=["PUT"])
def handle_add_user_to_db(user_id: str):
    try:
        fuser = FirebaseUser.get_user_by_uid(user_id)
    except UserNotFoundError:
        return Error("User not found").to_json(400)
    except FirebaseError as e:
        print("FirebaseError:", e)
        return Error("Internal error").to_json(500)

    try:
        user = User.from_firebase_user(fuser)
    except UserAlreadyExistsError:
        return Error("User already exists").to_json(409)
    except PostgresError as e:
        print("FirebaseError:", e)
        return Error("Internal server error").to_json(500)

    return vars(user), 201


# Update a single user's info (including accepted currencies)
@app.route("/user/<user_id>", methods=["PATCH"])
def handle_update_user(user_id: str):
    return "", 204


# MESSAGES
# Get all messages from and to a user
@app.route("/user/<user_id>/conversations", methods=["GET"])
def handle_get_user_conversations(user_id: str):
    try:
        result = Message.get_messages_by_user_id(user_id)
        return result, 200
    except UserNotFoundError:
        return Error("User with given ID not found").to_json(400)
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)


# Send a single new message to another user
@app.route("/message", methods=["POST"])
def handle_send_message():
    data = request.get_json()

    try:
        sender_id = data["sender_id"]
    except KeyError:
        return Error("Missing field: sender_id").to_json(400)

    try:
        receiver_id = data["receiver_id"]
    except KeyError:
        return Error("Missing field: receiver_id").to_json(400)

    try:
        content = data["content"]
    except KeyError:
        return Error("Missing field: content").to_json(400)

    try:
        m = Message.new_message_with_ids(sender_id, receiver_id, content)
        m.send()
    except UserNotFoundError:
        return Error("At least one of the users not found").to_json(400)
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)

    return vars(m), 201


# CURRENCIES
# Get all currencies accepted by the system
@app.route("/currencies", methods=["GET"])
def handle_get_all_currencies():
    try:
        c = Currency.get_currencies()
        return c, 200
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error").to_json(500)


# MISCELLANEOUS
# Check the server's status
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
