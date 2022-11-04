from db import execute
from dataclasses import dataclass
from datetime import datetime

from users import User


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Price:
    price: int
    currency: str

    def __str__(self):
        pass

    def __repr__(self):
        pass


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Offer:
    id: str
    title: str
    description: str
    price: Price
    seller: User
    images: list[str]
    created_at: datetime

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        pass


def get_all_offers() -> tuple[Offer]:
    pass


def get_offer_by_id(offer_id: str) -> Offer:
    pass


def get_offers_by_user_id(user_id: str) -> tuple[Offer]:
    pass


def add_offer(offer: Offer):
    pass
