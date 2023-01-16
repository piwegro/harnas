from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"

import unittest
import db


class db_test(unittest.TestCase):
    def test_connect(self):
        db.connect()
        self.assertIsNotNone(db.connection)

    def test_disconnect(self):
        db.connect()
        db.disconnect()
        self.assertIsNone(db.connection)

    def test_execute(self):
        db.connect()
        db.execute("SELECT 1", ())
        db.disconnect()

    def test_execute_with_params(self):
        db.connect()
        db.execute("SELECT %s", (1,))
        db.disconnect()

    def test_fetch(self):
        db.connect()
        db.execute("DELETE FROM piwegro.currencies", ())
        db.execute("INSERT INTO piwegro.currencies (symbol, name, exchange_rate) VALUES (%s, %s, %s)", ('PER', 'Perla', 1.0))
        result = db.fetch("SELECT * FROM piwegro.currencies", ())
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
