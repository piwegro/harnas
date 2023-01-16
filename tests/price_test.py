import unittest
from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"

from currencies import Price, Currency

class price_test(unittest.TestCase):
    def test_str(self):
        currency = Currency('Harnas', 'HAR', 1.0)
        price = Price(1, currency)

        self.assertEqual(str(price), 'Price(price="1", currency="Harnas")')

    def test_repr(self):
        currency = Currency('Harnas', 'HAR', 1.0)
        price = Price(1, currency)

        self.assertEqual(repr(price), 'Price("1", "Harnas")')

    def test_convert_to(self):
        currency = Currency('Harnas', 'HAR', 4.0)
        price = Price(1, currency)
        currency2 = Currency('US Dollar', 'USD', 2.0)

        converted = price.convert_to(currency2)

        self.assertEqual(converted.amount, 2)
