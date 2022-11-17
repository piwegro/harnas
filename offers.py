# Types import
from datetime import datetime
from dataclasses import dataclass
from users import User
from currencies import Currency, Price
from typing import Optional, List
from images import Image

# Exceptions
from exc import OfferNotFoundError, UserNotFoundError, CurrencyNotFoundError, PostgresError

# Functions import
from db import fetch, execute

RESULTS_PER_PAGE = 15


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Offer:
    id: Optional[str]
    title: str
    description: str
    price: Price
    seller: User
    images: List[Image]
    location: str
    created_at: datetime

    is_added = property(lambda self: self.id is not None)

    @classmethod
    def new_offer(cls, title: str, description: str, price: Price,
                  seller: User, location: str, images: List[Image]) -> "Offer":
        """
        Creates a new offer.

        :param title: The title of the offer.
        :param description: The description of the offer.
        :param price: The price of the offer.
        :param seller: The seller.
        :param location: The location of the offer.
        :param images: The list of links to the images.

        :return: The new offer.
        """
        return cls(None, title, description, price, seller, location, images, datetime.now())

    @classmethod
    def new_offer_with_id(cls, title: str, description: str, currency_symbol: str, amount: int,
                          seller_id: str, location: str, images: List[Image]) -> "Offer":
        """
        Creates a new offer, but with seller id instead of seller object.

        :param title: The title of the offer.
        :param description: The description of the offer.
        :param currency_symbol: The symbol of the currency.
        :param amount: The amount of the currency.
        :param seller_id: The id of the seller.
        :param location: The location of the offer.
        :param images: The list of links to the images.

        :raises UserNotFoundError: If the user with the given id does not exist.
        :raises CurrencyNotFoundError: If the currency with the given symbol does not exist.

        :return: The new offer.
        """
        try:
            seller = User.get_user_by_id(seller_id)
            currency = Currency.get_currency_by_symbol(currency_symbol)
        except UserNotFoundError:
            raise
        except CurrencyNotFoundError:
            raise

        return cls(None, title, description, Price(amount, currency), seller, images, location, datetime.now())

    @classmethod
    def new_offer_from_row(cls, raw_offer) -> "Offer":
        """
                Create a new offer from a row of the database

                :param raw_offer:
                :return: an offer
                """
        try:
            currency = Currency.get_currency_by_symbol(raw_offer[5])
            user = User.get_user_by_id(raw_offer[1])
        except UserNotFoundError:
            raise
        except CurrencyNotFoundError:
            raise

        return cls(raw_offer[0], raw_offer[2], raw_offer[3],
                   Price(raw_offer[4], currency), user, Image.dummies(), raw_offer[8], raw_offer[7])

    def add(self) -> None:
        """
        Adds the offer to the database.

        :raises PostgresError: If the offer could not be added to the database.
        """
        execute("INSERT INTO offers (seller_id, name, description, price, currency, created_at, location) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (self.seller.uid, self.title, self.description, self.price.amount, self.price.currency.symbol,
                 self.created_at, self.location))

        result = fetch("SELECT id FROM offers WHERE seller_id = %s AND name = %s AND description = %s "
                       "AND price = %s AND currency = %s AND created_at = %s AND location = %s",
                       "ORDER BY created_at DESC LIMIT 1",
                       (self.seller.uid, self.title, self.description, self.price.amount,
                        self.price.currency.symbol, self.created_at, self.location))

        if result is None or len(result) == 0:
            raise PostgresError("The offer was not added to the database.")

        self.id = result[0][0]

    @classmethod
    def get_all_offers(cls) -> list["Offer"]:
        """
        Get all offers from the database

        :return: list of offers
        :raises: PostgresError if there is no offers in the database
        """
        result = fetch("SELECT * FROM offers", ())

        list_of_offers = []

        for offer in result:
            list_of_offers.append(cls.new_offer_from_row(offer))

        return list_of_offers

    @classmethod
    def search_offers(cls, query: str, page: int) -> list["Offer"]:
        """
        Search offers by query

        :param page: The page number.
        :param query: the query to search
        :return: list of offers
        """
        max_len = len(query)/2
        page_start = page * RESULTS_PER_PAGE
        result = fetch("SELECT * FROM piwegro.offers WHERE LEVENSHTEIN(LOWER(name), LOWER(%s)) < %s "
                       "ORDER BY LEVENSHTEIN(LOWER(name), LOWER(%s)) ASC LIMIT %s OFFSET %s ;",
                       (query, max_len, query, RESULTS_PER_PAGE, page_start))

        list_of_offers = []

        for offer in result:
            list_of_offers.append(cls.new_offer_from_row(offer))

        return list_of_offers

    @classmethod
    def get_offer_by_id(cls, offer_id: str) -> "Offer":
        """
        Get an offer by its id

        :param offer_id:
        :return: an offer
        :raises: PostgresError: if there is no offer with the given id
        """
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
        """
        Get all offers from the database

        :param user_id:
        :return: an offer
        :raises PostgresError is there is no offer from the user
        """
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
