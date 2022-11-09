from dataclasses import dataclass
from db import fetch
from exc import CurrencyNotFoundError


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Currency:
    """ Represents a single currency """
    name: str
    symbol: str
    value: float

    @classmethod
    def get_currencies(cls) -> list["Currency"]:
        """
        Gets all possible currencies from the database

        :return: A list of all currencies
        """
        c = []

        result = fetch("SELECT symbol, name, exchange_rate FROM currencies", ())
        if result is None:
            raise CurrencyNotFoundError("No currencies found")
        for raw_currency in result:
            currency = Currency(raw_currency[1], raw_currency[0], raw_currency[2])
            c.append(currency)

        return c

    @classmethod
    def get_currency_by_symbol(cls, symbol: str) -> "Currency":
        """
        Gets a currency by its symbol

        :param symbol: The symbol of the currency
        :return: The currency
        :raises CurrencyNotFoundError: If the currency does not exist
        """
        result = fetch("SELECT symbol, name, exchange_rate FROM currencies WHERE symbol = %s", (symbol,))
        if result is None:
            raise CurrencyNotFoundError(symbol)
        if len(result) > 1:
            raise CurrencyNotFoundError(symbol)
        raw_currency = result[0]
        if raw_currency is None:
            raise CurrencyNotFoundError(symbol)

        return cls(raw_currency[1], raw_currency[0], raw_currency[2])



    def __str__(self):
        return f'Currency(name="{self.name}", symbol="{self.symbol}", value="{self.value}")'

    def __repr__(self):
        return f'Currency("{self.name}", "{self.symbol}", "{self.value}")'


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Price:
    amount: int
    currency: Currency

    def __str__(self):
        return f'Price(price="{self.amount}", currency="{self.currency.name  }")'

    def __repr__(self):
        return f'Price("{self.price}", "{self.currency.name}")'
        

    def convert_to(self, other_currency: "Currency") -> "Price":
        value = self.value / other_currency.value
        if (value < 1):
            value = 1
        else:
            value = round(value, 0)

        return Price(value, other_currency)

