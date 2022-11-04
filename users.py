# Types import
from currencies import Currency
from dataclasses import dataclass
from firebase import FirebaseUser

# Exceptions
from exc import UserNotFoundError, PostgresError

# Functions import
from db import execute


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
        result = execute("SELECT id, email, name FROM users WHERE id = %s", (user_id,))
        if result is None or len(result) == 0:
            raise UserNotFoundError(user_id)

        if len(result) > 1:
            raise PostgresError("More than one user with the same id")

        raw_user = result[0]
        if raw_user is None:
            raise UserNotFoundError(user_id)

        user = cls(raw_user[0], raw_user[1], raw_user[2], [])

        result = execute("SELECT name, symbol, exchange_rate FROM currencies WHERE symbol IN "
                         "(SELECT currency_symbol FROM accepted_currencies WHERE user_id = %s)",
                         (user_id,))

        if result is None or len(result) == 0:
            raise PostgresError("No accepted currencies for user with id " + user_id)

        for raw_currency in result:
            currency = Currency(raw_currency[0], raw_currency[1], raw_currency[2])
            user.accepted_currencies.append(currency)

        return user

    # TODO: Implement, should check whether the user exists in the database (see insert_user),
    #  if not, add it to the database, with the default accepted currencies (HAR)
    @classmethod
    def from_firebase_user(cls, firebase_user: FirebaseUser):
        return cls(firebase_user.uid, firebase_user.email, firebase_user.name, [])

    # TODO: Implement, should add the accepted currency to the database (accepted_currencies) and then to
    #  the accepted_currencies list. Should also check whether the currency is already accepted and whether
    #  the currency exists in the database (currencies table). Should raise an exception if the currency
    #  does not exist or if some database error occurs.
    def add_accepted_currency(self, currency: Currency) -> None:
        pass

    # TODO: Implement, should remove the accepted currency from the database (accepted_currencies) and then from
    #  the accepted_currencies list. Should also check whether the currency is already accepted. Should raise an
    #  exception if some database error occurs.
    def remove_accepted_currency(self, currency: Currency) -> None:
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __str__(self):
        pass

    # TODO: Implement, see https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    def __repr__(self):
        pass

