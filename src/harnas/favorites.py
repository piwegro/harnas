from db import execute, fetch
from exc import PostgresError
from offers import Offer


def add_to_favorites(user_id: str, offer_id: int) -> None:
    try:
        execute("INSERT INTO favorites (user, offer) VALUES (%s, %s)", (user_id, offer_id))
    except Exception as e:
        raise PostgresError(e)


def remove_from_favorites(user_id, offer_id) -> None:
    try:
        execute("DELETE FROM favorites WHERE user = %s AND offer = %s", (user_id, offer_id))
    except Exception as e:
        raise PostgresError(e)

def get_user_favorites(user_id) -> list["Offer"]:
    try:
        result = fetch("SELECT * FROM offers WHERE id IN (SELECT offer FROM favorites WHERE user = %s)", (user_id,))
        o = []

        for row in result:
            o.append(Offer.new_offer_from_row(row))

        return o
    except Exception as e:
        raise PostgresError(e)