from dataclasses import dataclass
from db import execute

from exc import PostgresError, UserNotFoundError

from users import User


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class Review:
    reviewer: User
    reviewee: User
    review: str

    @classmethod
    def new_review_with_ids(cls, reviewer_id: str, reviewee_id: str, review: str) -> "Review":
        """
        Creates a new review with the user ids instead of the user objects.

        :param reviewer_id: The id of the reviewer.
        :param reviewee_id: The id of the reviewee.
        :param review: The review text.

        :raises UserNotFoundError: If the reviewer or the reviewee does not exist.
        :raises PostgresError: If the database error occurs

        :return: The created review.
        """
        try:
            reviewer = User.get_user_by_id(reviewer_id)
            reviewee = User.get_user_by_id(reviewee_id)
        except UserNotFoundError:
            raise

        return cls(reviewer, reviewee, review)

    def add(self) -> None:
        """
        Adds a review to the database. If the review for given reviewer-reviewee pair already exists, it is updated.

        :raises: PostgresError if the database error occurs
        :return: None
        """
        try:
            execute("DELETE FROM reviews WHERE reviewer = %s AND reviewee = %s", (self.reviewer.uid, self.reviewee.uid))

            execute("INSERT INTO reviews (reviewer, reviewee, review) VALUES (%s, %s, %s)",
                    (self.reviewer.uid, self.reviewee.uid, self.review))
        except Exception as e:
            raise PostgresError(e)
