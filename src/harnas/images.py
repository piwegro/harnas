from dataclasses import dataclass
from typing import List

from io import BytesIO
from base64 import b64decode
from uuid import uuid4
from os import environ
from pathlib import Path

from db import fetch, execute

from PIL import Image as PILImage
import pillow_heif


SIZES = [(96, 96), (200, 113), (1920, 1080)]
IMAGE_OUTPUT = environ["IMAGE_OUTPUT"]

pillow_heif.register_heif_opener()

@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Image:
    raw_image: PILImage.Image | None

    image_id: int | None

    original: str | None
    preview: str | None
    thumbnail: str | None

    @property
    def is_saved(self) -> bool:
        return self.image_id is not None and self.original is not None \
               and self.preview is not None and self.thumbnail is not None
    
    @property
    def is_editable(self) -> bool:
        return self.raw_image is not None

    @staticmethod
    def crop_center(img: PILImage.Image, crop_width: int, crop_height: int) -> PILImage.Image:
        """
        Crops the image to the center with the biggest possible size while maintaining the aspect ratio given by
        the crop width and height.

        :param img: The image to crop.
        :param crop_width: The width of the crop.
        :param crop_height: The height of the crop.

        :return: The cropped image.
        """
        ratio = crop_width / crop_height
        width, height = img.size

        if width / height > ratio:
            new_width = int(height * ratio)
            offset = int((width - new_width) / 2)
            resize = (offset, 0, width - offset, height)
        else:
            new_height = int(width / ratio)
            offset = int((height - new_height) / 2)
            resize = (0, offset, width, height - offset)

        img = img.crop(resize)
        img = img.resize((crop_width, crop_height), PILImage.ANTIALIAS)

        return img

    @classmethod
    def new_image_base64(cls, b64_image: str | bytes) -> "Image":
        """
        Creates an Image object from a base64 string.

        :param b64_image: The base64 string.
        :return: The image object.
        """
        try:
            img = PILImage.open(BytesIO(b64decode(b64_image)))
            return cls(img, None, None, None, None)
        except Exception:
            raise

    @classmethod
    def get_image_by_id(cls, image_id: int) -> "Image":
        """
        Gets the image with the given id.

        :param image_id: The id of the image.
        :return: The image.
        """

        result = fetch("SELECT original, preview, thumbnail FROM images WHERE id = %s", (image_id,))

        if len(result) == 0:
            raise Exception()

        return cls(None, image_id, result[0][0], result[0][1], result[0][2])

    @classmethod
    def get_images_by_offer_id(cls, offer_id: int) -> List["Image"]:
        """
        Gets all images of the offer with the given id.

        :param offer_id: The id of the offer.
        :return: A list of images.
        """
        results = fetch("SELECT id, original, preview, thumbnail FROM images "
                        "WHERE offer_id = %s", (offer_id,))

        return [cls(None, result[0], result[1], result[2], result[3]) for result in results]

    @classmethod
    def dummies(cls) -> List["Image"]:
        images = []

        for i in range(0, 3):
            images.append(cls(None, i, "https://dummyimage.com/1920x1080/000/fff.jpg&text=original",
                              "https://dummyimage.com/200x113/000/fff.jpg&text=preview",
                              "https://dummyimage.com/96x96/000/fff.jpg&text=thumbnail"))

        return images

    def save(self) -> None:
        """
        Saves the image both in the database and on the disk. Does nothing if the image is already saved.

        :return: None
        """
        if self.is_saved:
            return

        if not self.is_editable:
            raise Exception()

        group_name = str(uuid4())

        original = self.crop_center(self.raw_image, SIZES[0][0], SIZES[0][1])
        original_name = group_name + "_original.jpg"
        original_path = Path(IMAGE_OUTPUT, original_name)
        original.save(original_path, "JPEG")
        self.original = original_name

        preview = self.crop_center(self.raw_image, SIZES[1][0], SIZES[1][1])
        preview_name = group_name + "_preview.jpg"
        preview_path = Path(IMAGE_OUTPUT, preview_name)
        preview.save(preview_path, "JPEG")
        self.preview = preview_name

        thumbnail = self.crop_center(self.raw_image, SIZES[2][0], SIZES[2][1])
        thumbnail_name = group_name + "_thumbnail.jpg"
        thumbnail_path = Path(IMAGE_OUTPUT, thumbnail_name)
        thumbnail.save(thumbnail_path, "JPEG")
        self.thumbnail = thumbnail_name


        result = fetch("INSERT INTO images(original, preview, thumbnail) VALUES (%s, %s, %s) RETURNING id",
                (original_name, preview_name, thumbnail_name))

        self.image_id = int(result[0][0])


    def associate_with_offer(self, offer_id: int) -> None:
        """
        Associates the image with the offer with the given id.

        :param offer_id: The id of the offer.
        :return: None
        """
        if not self.is_saved:
            raise Exception()

        execute("UPDATE images SET offer_id = %s WHERE id = %s", (offer_id, self.image_id))