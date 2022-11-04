from datetime import datetime
from users import User
from dataclasses import dataclass


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Message:
    message_id: str
    sender: User
    receiver: User
    content: str
    sent_at: datetime

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        pass


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Conversation:
    conversation_id: str
    messages: list[Message]

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self) -> str:
        return ""

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self) -> str:
        return ""


# TODO: Implement, should get a list of conversations for a user
#  Should raise an exception if the operation fails
def get_conversations_by_user_id(user_id: str) -> list[Conversation]:
    return []


# TODO: Implement, should get a single conversations for an id
#  Should raise an exception if the operation fails or if the conversation does not exist
def get_conversation_by_id(conversation_id: str) -> Conversation:
    return Conversation("", [])


# TODO: Implement, should send a message (put it in the database)
def send_message(message: Message) -> None:
    return
