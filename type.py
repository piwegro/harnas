from dataclasses import dataclass
from datetime import datetime

from firebase_admin import auth


@dataclass
class Currency:
    name: str
    symbol: str
    value: float


class User:
    uid: str
    email: str
    name: str

    accepted_currencies: list[Currency]

    def __init__(self, uid: str, email: str, name: str):
        self.uid = uid
        self.email = email
        self.name = name

        self.accepted_currencies = []

    @classmethod
    def from_user_record(cls, user_record: auth.UserRecord):
        return cls(user_record.email, user_record.display_name, user_record.uid)


@dataclass
class Price:
    price: int
    currency: str


@dataclass
class Offer:
    id: str
    title: str
    description: str
    price: Price
    seller: User
    images: list[str]
    created_at: datetime


@dataclass
class Message:
    id: str
    sender: User
    receiver: User
    content: str
    sent_at: datetime


@dataclass
class Conversation:
    id: str
    messages: list[Message]
