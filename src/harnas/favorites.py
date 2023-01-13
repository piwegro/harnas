from db import execute, fetch
from exc import PostgresError
from offers import Offer


def add_to_favorites(user_id: str, offer_id: int) -> None:
    """
    Adds an offer to the favorites of the user.

    :param user_id: ID of the user
    :param offer_id: ID of the offer to add to the favorites
    :raises PostgresError: if the internal error occurs
    """
    try:
        execute("INSERT INTO favorites (\"user\", offer) VALUES (%s, %s)", (user_id, offer_id))
    except PostgresError:
        raise


def remove_from_favorites(user_id, offer_id) -> None:
    """
    Removes an offer from the favorites of the user.

    :param user_id: ID of the user
    :param offer_id: ID of the offer to remove from the favorites
    :raises PostgresError: if the internal error occurs
    """
    try:
        execute("DELETE FROM favorites WHERE user = %s AND offer = %s", (user_id, offer_id))
    except PostgresError:
        raise

def get_user_favorites(user_id) -> list["Offer"]:
    """
    Gets the favorites of the given user.

    :param user_id: ID of the user
    :raises PostgresError: if the internal error occurs
    """
    try:
        result = fetch("SELECT * FROM offers WHERE id IN (SELECT offer FROM favorites WHERE user = %s)", (user_id,))
        o = []

        for row in result:
            o.append(Offer.new_offer_from_row(row))

        return o
    except PostgresError:
        raise