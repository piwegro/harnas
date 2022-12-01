from dataclasses import dataclass

from users import User


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Review:
    reviewer: User
    reviewee: User
    review: str
