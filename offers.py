from dataclasses import dataclass
from datetime import datetime

from users import User
from currencies import Currency, Price


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Offer:
    id: str
    title: str
    description: str
    price: Price
    seller: User
    images: list[str]
    created_at: datetime

    # TODO: Should add an offer to the database and then return the offer
    @classmethod
    def new_offer(cls, title: str, description: str, price: Price, seller: User, images: list[str]) -> "Offer":
        return cls("", "", "", Price(0, Currency("", "", 1.0)), User("", "", "", []), [], datetime.now())

    @classmethod
    def get_all_offers(cls) -> list["Offer"]:
        return []

    @classmethod
    def get_offer_by_id(cls, offer_id: str) -> "Offer":
        return cls("", "", "", Price(0, Currency("", "", 1.0)), User("", "", "", []), [], datetime.now())

    @classmethod
    def get_offers_by_user_id(cls, user_id: str) -> list["Offer"]:
        return []

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        pass
