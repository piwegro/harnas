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

    def __init__(self, email: str, name: str, uid: str):
        self.email = email
        self.name = name
        self.uid = uid

    @staticmethod
    def from_user_record(user_record: auth.UserRecord):
        return User(user_record.email, user_record.display_name, user_record.uid)


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
