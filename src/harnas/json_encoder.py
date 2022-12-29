from flask.json import JSONEncoder
from flask import jsonify

from typing import Any, Callable

from error import Error
from currencies import Currency
from images import Image
from messages import Message
from offers import Offer
from users import User

from datetime import datetime
from os import environ

ROOT_URL = environ["ROOT_URL"]


# TODO: Refactor
def as_json(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        if isinstance(result, tuple):
            o = result[0]
        else:
            o = result

        if isinstance(o, Error) or isinstance(o, Currency) or isinstance(o, Image) \
                or isinstance(o, Message) or isinstance(o, Offer) or isinstance(o, User):
            o = jsonify(o)

        if isinstance(result, tuple):
            return o, result[1]

        return o

    wrapper.__name__ = func.__name__
    return wrapper


class APIEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Error):
            return {
                'error': obj.message
            }

        if isinstance(obj, Offer):
            return {
                'offer_id': obj.offer_id,
                'title': obj.title,
                'description': obj.description,
                'price': obj.price,
                'seller': obj.seller,
                'images': obj.images,
                'location': obj.location,
                'created_at': obj.created_at
            }

        if isinstance(obj, Currency):
            return {
                'symbol': obj.symbol,
                'name': obj.name
            }

        if isinstance(obj, Image):
            # Temporary solution
            # TODO: Remove after updating the database
            if "http" in obj.original:
                return {
                    'image_id': obj.image_id,
                    'original': obj.original,
                    'preview': obj.preview,
                    'thumbnail': obj.thumbnail
                }

            original_url = ROOT_URL + '/images/' + obj.original
            preview_url = ROOT_URL + '/images/' + obj.preview
            thumbnail_url = ROOT_URL + '/images/' + obj.thumbnail

            return {
                'image_id': obj.image_id,
                'original': original_url,
                'preview': preview_url,
                'thumbnail': thumbnail_url
            }

        if isinstance(obj, Message):
            return {
                'message_id': obj.message_id,
                'sender': obj.sender,
                'receiver': obj.receiver,
                'content': obj.content,
                'sent_at': obj.sent_at
            }

        if isinstance(obj, User):
            return {
                'uid': obj.uid,
                'name': obj.name,
                'accepted_currencies': obj.accepted_currencies
            }

        if isinstance(obj, datetime):
            return obj.isoformat()

        return super().default(obj)
