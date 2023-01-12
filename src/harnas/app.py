# Flask import
from flask import Flask, request, make_response, send_from_directory
from flask_cors import CORS

# Exceptions import
from exc import PostgresError, FirebaseError, \
    UserNotFoundError, UserAlreadyExistsError, CurrencyNotFoundError, OfferNotFoundError


# Functions and classes import
from currencies import Currency
from error import Error
from firebase import FirebaseUser, initialize_firebase, verify_token
from review import Review
from health import check_health
from images import Image
from messages import Message
from offers import Offer
from users import User
from favorites import add_to_favorites, remove_from_favorites, get_user_favorites

from json_encoder import APIEncoder, as_json
from os import environ

app = Flask(__name__)
app.json_encoder = APIEncoder

CORS(app)

initialize_firebase()

IMAGE_PATH = environ["IMAGE_OUTPUT"]

# GETTING OFFERS
# Get a single offer by  its id
@app.route("/offer/<offer_id>", methods=["GET"])
@as_json
def hande_get_offer_by_id(offer_id: str):
    try:
        return Offer.get_offer_by_id(offer_id), 200
    except OfferNotFoundError:
        return Error("Offer not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Get all offers for a query (paginated)
@app.route("/offers/search/<query>/<page>", methods=["GET"])
@as_json
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
@app.route("/offers/<page>", methods=["GET"])
@as_json
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
@app.route("/user/<user_id>/offers", methods=["GET"])
@as_json
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
@app.route("/offer", methods=["POST"])
@as_json
def handle_add_offer():
    # TODO: Handle it better
    try:
        seller_id = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

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
        location = None

    try:
        images = data["images"]
    except KeyError:
        return Error("Missing field: 'images'"), 400

    try:
        price = int(price)
    except ValueError:
        return Error("Invalid price"), 400

    try:
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
@app.route("/image", methods=["POST"])
@as_json
def handle_post_images():
    # TODO: Handle it better
    try:
        verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    body = request.get_data(cache=False)

    try:
        img = Image.new_image_base64(body)
        img.save()
        return img, 201

    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Handle images
@app.route("/image/<path:path>", methods=["GET"])
def handle_get_image(path: str):
    return send_from_directory(IMAGE_PATH, path)


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
@app.route("/user/<user_id>", methods=["PATCH"])
@as_json
def handle_update_user(user_id: str):
    return None, 204


# MESSAGES
# Get all messages beetwen two users
@app.route("/messages/<user_id>", methods=["GET"])
@as_json
def handle_get_conversation(user_id: str):
    try:
        current_user = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        return Message.get_messages_beetween_user_ids(user_id, current_user), 200
    except UserNotFoundError:
        return Error("User not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Get all messages from and to a user
@app.route("/messages", methods=["GET"])
@as_json
def handle_get_user_conversations():
    # TODO: Handle it better
    try:
        user_id = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        result = Message.get_messages_by_user_id(user_id)
        return result, 200
    except UserNotFoundError:
        return Error("User with given ID not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# Send a single new message to another user
@app.route("/message", methods=["POST"])
@as_json
def handle_send_message():
    # TODO: Handle it better
    try:
        sender_id = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    data = request.get_json(cache=False)

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
@app.route("/currencies", methods=["GET"])
@as_json
def handle_get_all_currencies():
    try:
        return Currency.get_currencies(), 200
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# REVIEWS
# Add a new review (or update an existing one)
@app.route("/review", methods=["POST"])
@as_json
def handle_add_review():
    data = request.get_json()

    # TODO: Handle it better
    try:
        reviewer_id = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        reviewee_id = data["reviewee_id"]
    except KeyError:
        return Error("Missing field: 'reviewee_id'"), 400

    try:
        content = data["review"]
    except KeyError:
        return Error("Missing field: 'content'"), 400

    try:
        r = Review.new_review_with_ids(reviewer_id, reviewee_id, content)
        r.add()
    except UserNotFoundError:
        return Error("At least one of the users not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500

    return r, 201


# Get all reviews for a user
@app.route("/reviews/<user_id>", methods=["GET"])
@as_json
def handle_get_reviews(user_id: str):
    try:
        return Review.get_reviews_for_user_id(user_id), 200
    except UserNotFoundError:
        return Error("User not found"), 400
    except Exception as e:
        print("Exception:", e)
        return Error("Internal server error"), 500


# FAVORITES
# Add an offer to a user's favorites
@app.route("/favorites/<offer_id>", methods=["PUT"])
@as_json
def handle_add_favorite(offer_id):
    # TODO: Handle it better
    try:
        user = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        add_to_favorites(user, offer_id)
        return get_user_favorites(user), 201
    except Exception as e:
        print("Exception:", e)
        return Error("Error"), 401


# Remove an offer from a user's favorites
@app.route("/favorites/<offer_id>", methods=["DELETE"])
@as_json
def handle_remove_favorite(offer_id):
    # TODO: Handle it better
    try:
        user = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        remove_from_favorites(user, offer_id)
        return get_user_favorites(user), 200
    except Exception as e:
        print("Exception:", e)
        return Error("Error"), 401


# Get the user favorites
@app.route("/favorites")
@as_json
def handle_get_favorites():
    # TODO: Handle it better
    try:
        user = verify_token(request.headers["Authorization"].split(" ")[1])
    except Exception as e:
        print("Exception:", e)
        return Error("Unauthorized"), 401

    try:
        return get_user_favorites(user), 200
    except Exception as e:
        print("Exception:", e)
        return Error("Error"), 401


# MISCELLANEOUS
# Check the server's status
@app.route("/health", methods=["GET"])
@as_json
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
