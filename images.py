from dataclasses import dataclass
from typing import List


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Image:
    image_id: int
    original: str
    preview: str
    thumbnail: str

    @classmethod
    def dummies(cls) -> List["Image"]:
        images = []

        for i in range(0, 3):
            images.append(cls(i, "https://dummyimage.com/1920x1080/000/fff.jpg&text=original",
                              "https://dummyimage.com/200x113/000/fff.jpg&text=preview",
                              "https://dummyimage.com/96x96/000/fff.jpg&text=thumbnail"))

        return images
