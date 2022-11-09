from flask import Flask, request

from users import User
from currencies import Currency
from firebase import FirebaseUser, initialize_firebase
from health import check_health
from messages import Message

app = Flask(__name__)
initialize_firebase()


# GETTING OFFERS
# Get a single offer by  its id
@app.route("/offer/<id>", methods=["GET"])
def hande_get_offer_by_id(offer_id: str):
    return "WIP"


# Get all offers for a query (paginated)
@app.route("/offers/search/<query>/<page>", methods=["GET"])
def handle_get_offers_by_query(query: str, page: str):
    return "WIP"


# Get all offers (paginated)
@app.route("/offers/<page>", methods=["GET"])
def handle_get_all_offers():
    return "WIP"


# Get all offers by a user id (not paginated)
@app.route("/user/<id>/offers", methods=["GET"])
def handle_get_offers_by_user_id(user_id: str):
    return "WIP"


# ADDING OFFERS
# Add a single offer
@app.route("/offer", methods=["POST"])
def handle_add_offer():
    return "WIP"


# USER MANAGEMENT
# Get a single user's info (including accepted currencies) by its id
@app.route("/user/<user_id>", methods=["GET"])
def handle_user_by_id(user_id: str):
    user = User.get_user_by_id(user_id)
    return vars(user)


# Put a new user in the database (after sign up)
@app.route("/user/<user_id>", methods=["PUT"])
def handle_add_user_to_db(user_id: str):
    fuser = FirebaseUser.get_user_by_uid(user_id)
    user = User.from_firebase_user(fuser)
    return vars(user)


# Update a single user's info (including accepted currencies)
@app.route("/user/<user_id>", methods=["PATCH"])
def handle_update_user(user_id: str):
    return "WIP"


# MESSAGES
# Get all messages from and to a user
@app.route("/user/<user_id>/conversations", methods=["GET"])
def handle_get_user_conversations(user_id: str):
    result = Message.get_messages_by_user_id(user_id)
    return result


# Send a single new message to another user
@app.route("/message", methods=["POST"])
def handle_send_message():
    data = request.get_json()
    m = None

    try:
        sender_id = data["sender_id"]
        receiver_id = data["receiver_id"]
        content = data["content"]
    except KeyError:
        return "Missing parameter", 400

    try:
        m = Message.new_message_with_ids(sender_id, receiver_id, content)
        m.send()
    except Exception as e:
        return "Error: " + str(e), 500

    return vars(m)


# CURRENCIES
# Get all currencies accepted by the system
@app.route("/currencies", methods=["GET"])
def handle_get_all_currencies():
    c = Currency.get_currencies()
    return c


# MISCELLANEOUS
# Check the server's status
@app.route("/health", methods=["GET"])
def handle_health():
    status, message = check_health()
    return {
        "healthy": status,
        "message": message
    }


# Handle root queries
@app.route("/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def handle_root():
    return "You've reached the root of the internal Piwegro API. Unfortunately, there's nothing here."
