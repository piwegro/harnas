import firebase_admin

from firebase_admin import credentials, auth
from exc import FirebaseNotInitializedError
from type import User

firebase_app = None


def initialize_firebase():
    global firebase_app
    if firebase_app is not None:
        return

    cred = credentials.Certificate('serviceAccountKey.json')

    firebase_app = firebase_admin.initialize_app(cred)


def get_user_info(uid: str) -> User:
    global firebase_app
    if firebase_app is None:
        raise FirebaseNotInitializedError()

    user_record = auth.get_user(uid)
    return User.from_user_record(user_record)


def verify_token(token: str):
    global firebase_app
    if firebase_app is None:
        raise FirebaseNotInitializedError()

    try:
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        uid = decoded_token['uid']
        return uid
    except auth.RevokedIdTokenError:
        return None
    except auth.UserDisabledError:
        return None
    except auth.InvalidIdTokenError:
        return None
    except Exception:
        raise
