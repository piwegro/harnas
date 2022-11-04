from flask import Flask, request

from users import User
from currencies import Currency
from firebase import FirebaseUser, initialize_firebase
from health import check_health


app = Flask(__name__)

initialize_firebase()


# All offers (paginated)
@app.route("/offers/<page>")
def handle_get_all_offers():
    return "WIP"


# Singe offer by id
@app.route("/offer/<id>")
def hande_get_offer_by_id(offer_id: str):
    return "WIP"


# User info
@app.route("/user/<user_id>")
def handle_user_by_id(user_id: str):
    user = User.get_user_by_id(user_id)
    return vars(user)


@app.route("/user/<user_id>", methods=["PUT"])
def handle_add_user_to_db(user_id: str):
    fuser = FirebaseUser.get_user_by_uid(user_id)
    user = User.from_firebase_user(fuser)
    return vars(user)


# All offers by user (not paginated [?])
@app.route("/user/<id>/offers")
def handle_get_offers_by_user_id(user_id: str):
    return "WIP"


# Get all conversations for user
@app.route("/user/<id>/conversations")
def handle_get_user_conversations(user_id: str):
    return "WIP"


# Get a single conversation
@app.route("/conversation/<id>")
def handle_get_conversation_by_id(conversation_id: str):
    return "WIP"


# Send a message to a conversation
@app.route("/message", methods=["POST"])
def handle_send_message(req):
    return "WIP"


# Get all currencies
@app.route("/currencies")
def handle_get_all_currencies():
    c = Currency.get_currencies()
    return c


@app.route("/health")
def handle_health():
    status, message = check_health()
    return {
        "healthy": status,
        "message": message
    }
