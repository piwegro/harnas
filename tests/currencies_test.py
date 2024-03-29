from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"

import unittest
from currencies import Currency
import db
import exc

class currencies_test(unittest.TestCase):

    def test_str(self):
        currency = Currency('US Dollar', 'USD', 1.0)
        self.assertEqual(str(currency), 'Currency(name="US Dollar", symbol="USD", value="1.0")')

    def test_repr(self):
        currency = Currency('US Dollar', 'USD', 1.0)
        self.assertEqual(repr(currency), 'Currency("US Dollar", "USD", "1.0")')

    def test_get_all(self):
        db.connect()
        db.execute("DELETE FROM piwegro.currencies", ())
        db.execute("INSERT INTO piwegro.currencies (symbol, name, exchange_rate) VALUES (%s, %s, %s)", ('PER', 'Perla', 1.0))
        result = Currency.get_currencies()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'Perla')
        db.disconnect()

    def test_get_all_if_empty(self):
        db.connect()
        db.execute("DELETE FROM piwegro.currencies", ())
        self.assertEqual(len(Currency.get_currencies()), 0)

    def test_get_by_symbol(self):
        db.connect()
        db.execute("DELETE FROM piwegro.currencies", ())
        db.execute("INSERT INTO piwegro.currencies (symbol, name, exchange_rate) VALUES (%s, %s, %s)", ('PER', 'Perla', 1.0))
        result = Currency.get_currency_by_symbol('PER')
        self.assertEqual(result.name, 'Perla')
        self.assertTrue(isinstance(result, Currency))
        db.disconnect()
