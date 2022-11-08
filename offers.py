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

    def __str__(self):
        return f'Offer(id="{self.id}", title="{self.title}", description="{self.description}", ' \
               f'price="{self.price.amount}", currency="{self.price.currency}", seller\' id="{self.seller.uid}", ' \
               f'images="{self.images}", created_at="{self.created_at.min}")'

    def __repr__(self):
        return f'Offer("{self.id}", "{self.title}", "{self.description}", "{self.price.amount}", ' \
               f'"{self.price.currency}", "{self.seller.uid}", "{self.images}", "{self.created_at.min}")'
