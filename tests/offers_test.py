from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"
environ["SERVICE_ACCOUNT_PATH"] = "test/path"
environ["IMAGE_OUTPUT"] = "test/output"

import unittest
from offers import Offer
from currencies import Currency, Price
from users import User
import db

class offers_test(unittest.TestCase):

    def test_new_offer(self):
        cur = Currency('Perla', 'PER', 1.0)
        price = Price(cur, 100)
        user = User('1', 'Anna', 'anna@mail.com', '', '')
        offer = Offer.new_offer('test', 'test', price, user, {}, 'test')
        self.assertTrue(isinstance(offer, Offer))

    def test_new_offer_with_id(self):
        cur = Currency('Perla', 'PER', 1.0)
        price = Price(cur, 100)
        # user = User('1', 'Anna', 'anna@mail.com', '', '')
        db.connect()
        db.execute("INSERT INTO piwegro.users (id, name, email) VALUES ('5', 'Kasia', 'kasia@mail.com')", ())
        offer = Offer.new_offer_with_id('test', 'test', 'PER', 1,'5', '', 'test')
        self.assertTrue(isinstance(offer, Offer))
        db.execute("DELETE FROM piwegro.users WHERE id='5'", ())
        db.disconnect()


