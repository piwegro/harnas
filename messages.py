from typing import Optional

from datetime import datetime

from users import User
from dataclasses import dataclass
from db import execute, fetch


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Message:
    message_id: Optional[str]

    sender: User
    receiver: User
    content: str
    sent_at: datetime

    is_sent: bool = False

    @classmethod
    def new_message_with_ids(cls, sender_id: str, receiver_id: str, content: str,
                             sent_at: datetime = datetime.now()) -> "Message":
        """
        Creates a new message with the user ids instead of the user objects.

        :param sender_id: The id of the sender.
        :param receiver_id: The id of the receiver.
        :param content: The content of the message.
        :param sent_at: The time the message was sent.
        :return: The created message.
        """
        return cls(None, User.get_user_by_id(sender_id), User.get_user_by_id(receiver_id), content, sent_at)

    @classmethod
    def new_message(cls, sender: User, receiver: User, content: str, sent_at: datetime = datetime.now()) -> "Message":
        """
        Creates a new message object without an id. Note that the message is not sent until the send_message method is
        called.

        :param sender: The user that sends the message.
        :param receiver: The user that receives the message.
        :param content: The content of the message.
        :param sent_at: The time when the message was sent. Defaults to the current time.
        :return: A new message object.
        """
        return cls(None, sender, receiver, content, sent_at)

    # TODO: Handle errors
    def send(self) -> None:
        """
        Sends the message to the database.

        :raise ValueError: If the message is already sent.
        """
        # TODO: Different exception type
        if self.is_sent:
            raise ValueError("Message already sent")

        execute("INSERT INTO messages (sender_id, receiver_id, content, sent_at) VALUES (%s, %s, %s, %s)",
                (self.sender.uid, self.receiver.uid, self.content, self.sent_at))

        result = fetch("SELECT id FROM messages WHERE sender_id = %s AND receiver_id = %s AND content = %s AND "
                       "sent_at = %s ORDER BY id DESC LIMIT 1",
                       (self.sender.uid, self.receiver.uid, self.content, self.sent_at))

        if result is None or len(result) == 0:
            raise RuntimeError("Message not found")

        self.message_id = result[0][0]
        self.is_sent = True

    @classmethod
    def get_messages_by_user_id(cls, user_id: str) -> list["Message"]:
        """
        Get all messages sent to or from a user.

        :param user_id: The id of the user.
        :return: A list of messages.
        """
        m = []

        result = fetch("SELECT * FROM messages WHERE sender_id = %s OR receiver_id = %s", (user_id, user_id))
        for raw_message in result:
            sender = User.get_user_by_id(raw_message[1])
            receiver = User.get_user_by_id(raw_message[2])
            m.append(cls(raw_message[0], sender, receiver, raw_message[3], raw_message[4], True))

        return m

    def __str__(self) -> str:
        return f"Message {self.message_id} from {self.sender.uid} to {self.receiver.uid} at {self.sent_at}"

    def __repr__(self) -> str:
        return f'Message("{self.message_id}", "{self.sender.uid}", "{self.receiver.uid}", "{self.content}", "{self.sent_at}")'
