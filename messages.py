from datetime import datetime
from users import User
from dataclasses import dataclass
from db import execute, fetch


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Message:
    message_id: str
    sender: User
    receiver: User
    content: str
    sent_at: datetime

    def send_message(self) -> None:
        result = execute("INSERT INTO messages (sender_id, receiver_id, content, sent_at) VALUES (%s, %s, %s, %s)",
                         (self.sender.uid, self.receiver.uid, self.content, self.sent_at))

    @classmethod
    def get_messages_by_user_id(cls, user_id: str) -> list["Message"]:
        m = []

        result = fetch("SELECT * FROM messages WHERE sender_id = %s OR receiver_id = %s", (user_id, user_id))
        for raw_message in result:
            sender = User.get_user_by_id(raw_message[1])
            receiver = User.get_user_by_id(raw_message[2])
            m.append(cls(raw_message[0], sender, receiver, raw_message[3], raw_message[4]))

        return m

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        pass
