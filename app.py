from flask import Flask, request

from users import get_user_by_id
from health import check_health

app = Flask(__name__)


# All offers (paginated)
@app.route("/offers/<page>")
def get_all_offers():
    return "WIP"


# Singe offer by id
@app.route("/offer/<id>")
def get_offer_by_id(offer_id: str):
    return "WIP"


# User info
@app.route("/user/<user_id>")
def handle_user_by_id(user_id: str):
    user = get_user_by_id(user_id)
    return vars(user)


# All offers by user (not paginated [?])
@app.route("/user/<id>/offers")
def get_offers_by_user_id(user_id: str):
    return "WIP"


# Get all conversations for user
@app.route("/user/<id>/conversations")
def get_user_conversations(user_id: str):
    return "WIP"


# Get a single conversation
@app.route("/conversation/<id>")
def get_conversation_by_id(conversation_id: str):
    return "WIP"


# Send a message to a conversation
@app.route("/message", methods=["POST"])
def send_message(req):
    return "WIP"


@app.route("/health")
def health():
    status, message = check_health()
    if status:
        return {
            "status": "ok",
            "message": None
        }
    else:
        return {
            "status": "error",
            "message": message
        }
