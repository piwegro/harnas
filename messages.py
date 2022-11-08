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

    # TODO: Implement, should get all user's messages
    @classmethod
    def get_messages_by_user_id(cls, user_id: str) -> list["Message"]:
        return []

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.uid} to {self.receiver.uid} at {self.sent_at}"

    def __repr__(self):
        return f'Message("{self.message_id}", "{self.sender.uid}", "{self.receiver.uid}", "{self.content}", "{self.sent_at}")'
