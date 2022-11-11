# Types import
from datetime import datetime
from dataclasses import dataclass
from users import User
from currencies import Currency, Price

# Exceptions
from exc import OfferNotFoundError

# Functions import
from db import fetch


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
    def new_offer_from_row(cls, raw_offer) -> "Offer":
        return cls(raw_offer[0], raw_offer[2], raw_offer[3],
                   Price(raw_offer[4], Currency.get_currency_by_symbol(raw_offer[5])),
                   User.get_user_by_id(raw_offer[1]), raw_offer[6], raw_offer[7])

    @classmethod
    def get_all_offers(cls) -> list["Offer"]:
        result = fetch("SELECT * FROM offers", ())

        list_of_offers = []

        for offer in result:
            list_of_offers.append(cls.new_offer_from_row(offer))

        return list_of_offers

    @classmethod
    def get_offer_by_id(cls, offer_id: str) -> "Offer":
        result = fetch("SELECT * from offers WHERE id = %s", (offer_id,))
        if result is None or len(result) == 0:
            raise OfferNotFoundError(f"Offer with id {offer_id} not found")

        raw_offer = result[0]
        if raw_offer is None:
            raise OfferNotFoundError(f"Offer with id {offer_id} not found")

        offer = cls.new_offer_from_row(raw_offer)
        return offer

    @classmethod
    def get_offers_by_user_id(cls, user_id: str) -> list["Offer"]:
        result = fetch("SELECT * from offers WHERE seller_id = %s", (user_id,))

        if result is None or len(result) == 0:
            raise OfferNotFoundError(f"No offers found for user {user_id}")

        raw_offer = result[0]
        if raw_offer is None:
            raise OfferNotFoundError(f"No offers found for user {user_id}")

        list_of_offers = []
        for offer in result:
            list_of_offers.append(cls.new_offer_from_row(offer))

        return list_of_offers

    def __str__(self):
        return f'Offer(id="{self.id}", title="{self.title}", description="{self.description}", ' \
               f'price="{self.price.amount}", currency="{self.price.currency.symbol}", seller\' id="{self.seller.uid}", ' \
               f'images="{self.images}", created_at="{self.created_at.min}")'

    def __repr__(self):
        return f'Offer("{self.id}", "{self.title}", "{self.description}", "{self.price.amount}", ' \
               f'"{self.price.currency}", "{self.seller.uid}", "{self.images}", "{self.created_at.min}")'
