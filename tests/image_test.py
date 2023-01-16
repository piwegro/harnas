from os import environ

environ["POSTGRES_HOST"] = "localhost"
environ["POSTGRES_USER"] = "postgres"
environ["POSTGRES_PASSWORD"] = "postgres"
environ["POSTGRES_DB_MAIN"] = "test_database"
environ["SERVICE_ACCOUNT_PATH"] = "temp/path"
environ["IMAGE_OUTPUT"] = "temp/path"

from images import Image

def test_from_base64():
    # Get base64 image from file
    with open('tests/files/base64.txt', 'r') as f:
        base64 = f.read()
        img = Image.new_image_base64(base64)

    assert img is not None


# def test_from_base64_save():
#     # Get base64 image from file
#     with open('tests/files/base64.txt', 'r') as f:
#         base64 = f.read()
#         img = Image.new_image_base64(base64)
#         img.save()
#
#     assert img is not None
