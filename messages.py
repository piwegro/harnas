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

    # TODO: Implement, should send a message (put it in the database) and raise an exception if it fails
    def send_message(self) -> None:
        return

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        return f'Message(message_id="{self.message_id}", sender\'s ID={self.sender.uid}, receiver\'s ID="{self.receiver.uid}", content="{self.content}", sent_at="{self.sent_at}")'

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        return f'Message("{self.message_id}", "{self.sender.uid}", "{self.receiver.uid}", "{self.content}", "{self.sent_at}")'



@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Conversation:
    conversation_id: str
    messages: list[Message]

    # TODO: Implement, should get a list of conversations for a user
    #  Should raise an exception if the operation fails
    @classmethod
    def get_conversations_by_user_id(cls, user_id: str) -> list["Conversation"]:
        return []

    # TODO: Implement, should get a single conversations for an id
    #  Should raise an exception if the operation fails or if the conversation does not exist
    @classmethod
    def get_conversation_by_id(cls, conversation_id: str) -> "Conversation":
        return Conversation("", [])

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self) -> str:
        return f'Conversation(id="{self.conversation_id}", messages="{self.messages}")'

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self) -> str:
        return f'Conversation("{self.conversation_id}", "{self.messages}")'

