from harnas.images import Image

def test_from_base64():
    # Get base64 image from file
    with open('tests/files/base64.txt', 'r') as f:
        base64 = f.read()
        img = Image.new_image_base64(base64)

    assert img is not None


def test_from_base64_save():
    # Get base64 image from file
    with open('tests/files/base64.txt', 'r') as f:
        base64 = f.read()
        img = Image.new_image_base64(base64)
        img.save()

    assert img is not None
