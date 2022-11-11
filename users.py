# Types import
from currencies import Currency
from dataclasses import dataclass
from firebase import FirebaseUser

# Exceptions
from exc import UserNotFoundError, CurrencyNotFoundError

# Functions import
from db import fetch, execute


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class User:
    uid: str
    email: str
    name: str

    accepted_currencies: list[Currency]

    @classmethod
    def get_user_by_id(cls, user_id: str) -> "User":
        """
        Get a user by its id
        :param user_id: The id of the user

        :return: The user
        :raises UserNotFoundError: If the user does not exist
        :raises PostgresError: If the database error occurs
        """
        result = fetch("SELECT id, email, name FROM users WHERE id = %s", (user_id,))
        if result is None or len(result) == 0 or result[0] is None:
            raise UserNotFoundError(user_id)

        raw_user = result[0]
        user = cls(raw_user[0], raw_user[1], raw_user[2], [])

        result = fetch("SELECT name, symbol, exchange_rate FROM currencies WHERE symbol IN "
                       "(SELECT currency_symbol FROM accepted_currencies WHERE user_id = %s)",
                       (user_id,))

        if len(result) == 0:
            # TODO: Probably an error if the user has no accepted currencies.
            #  Only possible when creating a user – should refactor
            print("No accepted currencies for user " + user_id)

        for raw_currency in result:
            currency = Currency(raw_currency[0], raw_currency[1], raw_currency[2])
            user.accepted_currencies.append(currency)

        return user

    # TODO: Should also check whether the currency is already accepted.
    def add_accepted_currency(self, currency: Currency) -> None:
        """
        Add an accepted currency to the user
        :param currency: Currency to add
        :return: None
        """
        result = fetch("SELECT count(*) FROM currencies WHERE symbol = %s", (currency.symbol,))
        if result is None or len(result) == 0 or result[0][0] == 0:
            raise CurrencyNotFoundError(currency.symbol)

        result = execute("INSERT INTO accepted_currencies (user_id, currency_symbol) VALUES (%s, %s)",
                         (self.uid, currency.symbol))

        self.accepted_currencies.append(currency)

    # TODO: Implement, should remove the accepted currency from the database (accepted_currencies) and then from
    #  the accepted_currencies list. Should also check whether the currency is already accepted. Should raise an
    #  exception if some database error occurs.
    def remove_accepted_currency(self, currency: Currency) -> None:
        pass

    @classmethod
    def from_firebase_user(cls, firebase_user: FirebaseUser) -> "User":
        """
        Create a user from a FirebaseUser by adding the accepted currencies and the user themselves
        to the postgres database

        :param firebase_user: The FirebaseUser
        :return: The new user
        """
        result = execute("INSERT INTO users (id, email, name) VALUES (%s, %s, %s)",
                         (firebase_user.uid, firebase_user.email, firebase_user.name))

        user = User.get_user_by_id(firebase_user.uid)
        # TODO: Handle default currency better
        user.add_accepted_currency(Currency("Harnaś", "HAR", 1.0))
        return user

    def __str__(self):
        return f'User(user_id="{self.uid}", email="{self.email}", name="{self.name}", accepted_currencies={self.accepted_currencies})'

    def __repr__(self):
        return f'User("{self.uid}", "{self.email}", "{self.name}", {self.accepted_currencies})'
