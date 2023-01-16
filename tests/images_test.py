from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"
environ["IMAGE_OUTPUT"] = "test_output"

import unittest
from harnas.exc import ImageNotFoundError
from harnas.images import Image
import harnas.db


class images_test(unittest.TestCase):

    def test_is_saved(self):
        img = Image(None, 1, 'test', 'test', 'test')
        self.assertTrue(img.is_saved)

    def test_is_not_saved(self):
        img = Image(None, None, None, None, None)
        self.assertFalse(img.is_saved)

    def test_is_not_editable(self):
        img = Image(None, 'test', 'test', 'test', 'test')
        self.assertFalse(img.is_editable)

    def test_is_editable(self):
        img = Image('test', 1, 'test', 'test', 'test')
        self.assertTrue(img.is_editable)

    def test_get_image_by_id(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.images", ())
        harnas.db.execute("INSERT INTO piwegro.images (id, offer_id, original, thumbnail, preview) VALUES (%s, %s, %s, %s, %s)", (1, 1, 'test', 'test', 'test'))
        result = Image.get_image_by_id(1)
        self.assertEqual(result.image_id, 1)
        harnas.db.disconnect()

    def test_get_image_by_id_not_found(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.images", ())
        with self.assertRaises(ImageNotFoundError) as context:
            Image.get_image_by_id(1)
        harnas.db.disconnect()

    def test_get_images_by_offer_id(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.images", ())
        harnas.db.execute("INSERT INTO piwegro.images (id, offer_id, original, thumbnail, preview) VALUES (%s, %s, %s, %s, %s)", (1, 1, 'test', 'test', 'test'))
        result = Image.get_images_by_offer_id(1)
        self.assertEqual(result[0].image_id, 1)
        harnas.db.disconnect()

    def test_dummies(self):
        images = Image.dummies()
        self.assertEqual(len(images), 3)

    def test_associate_with_offer(self):
        harnas.db.connect()
        harnas.db.execute("DELETE FROM piwegro.images", ())
        harnas.db.execute("DELETE FROM piwegro.offers WHERE id = 2", ())
        harnas.db.execute("INSERT INTO offers (id, seller_id, name, description, price, currency, images, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (2, 'KyumBFaY66ZdS3oG7fPZQZycKyC2', 'Półeczka', 'Bardzo ładna półeczka we wspaniałym stanie', 4, 'HAR', '{}', '2022-10-31 18:32:19.000000'))
        harnas.db.execute("INSERT INTO piwegro.images (id, offer_id, original, thumbnail, preview) VALUES (%s, %s, %s, %s, %s)", (1, 1, 'test', 'test', 'test'))
        img = Image.get_image_by_id(1)
        img.associate_with_offer(2)
        img = Image.get_image_by_id(1)
        result = harnas.db.fetch("SELECT offer_id FROM piwegro.images WHERE id = 1", ())
        self.assertEqual(result[0][0], 2)