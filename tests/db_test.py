from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"

import unittest
import harnas.db


class db_test(unittest.TestCase):
    def test_connect(self):
        harnas.db.connect()
        self.assertIsNotNone(harnas.db.connection)

    def test_disconnect(self):
        harnas.db.connect()
        harnas.db.disconnect()
        self.assertIsNone(harnas.db.connection)

    def test_execute(self):
        harnas.db.connect()
        harnas.db.execute("SELECT 1", ())
        harnas.db.disconnect()

    def test_execute_with_params(self):
        harnas.db.connect()
        harnas.db.execute("SELECT %s", (1,))
        harnas.db.disconnect()

    def test_fetch(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.currencies", ())
        harnas.db.execute("INSERT INTO piwegro.currencies (symbol, name, exchange_rate) VALUES (%s, %s, %s)", ('PER', 'Perla', 1.0))
        result = harnas.db.fetch("SELECT * FROM piwegro.currencies", ())
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()
