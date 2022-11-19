from flask.json import JSONEncoder

from error import Error
from currencies import Currency
from images import Image
from messages import Message
from offers import Offer
from users import User

from datetime import datetime


class APIEncoder(JSONEncoder):
    def default(self, obj):
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
            return {
                'image_id': obj.image_id,
                'original': obj.original,
                'preview': obj.preview,
                'thumbnail': obj.thumbnail
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
