from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"
environ["SERVICE_ACCOUNT_PATH"] = "test/path"

import unittest
from harnas.currencies import Currency
import harnas.db
import harnas.exc
import harnas.messages

class messages_test(unittest.TestCase):

    def test_get_messages_between_user_ids_user_not_found(self):
        harnas.db.connect()
        with self.assertRaises(harnas.exc.UserNotFoundError):
            harnas.messages.Message.get_messages_beetween_user_ids('100', '200')
        harnas.db.disconnect()

    def test_get_recipients(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.messages", ())
        harnas.db.execute("DELETE FROM piwegro.conversations", ())
        harnas.db.execute("DELETE FROM piwegro.users WHERE id='1' OR id='2'", ())
        harnas.db.execute("INSERT INTO piwegro.users (id, name, email) VALUES ('1', 'Anna', 'anna@mail.com')",())
        harnas.db.execute("INSERT INTO piwegro.users (id, name, email) VALUES ('2', 'Tomek', 'tomek@mail.com')", ())
        harnas.db.execute("INSERT INTO piwegro.conversations (id, user1_id, user2_id) VALUES ('222', '1', '2')", ())
        harnas.db.execute("INSERT INTO messages (id, conversation_id, sender_id, receiver_id, content) VALUES (1, '222', '1', '2', 'hello')", ())
        result = harnas.messages.Message.get_recipients('1')
        self.assertEqual(len(result), 1)

