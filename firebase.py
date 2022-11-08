import firebase_admin

from os import environ

from firebase_admin import credentials, auth
from exc import FirebaseNotInitializedError

from dataclasses import dataclass

SERVICE_ACCOUNT_PATH = environ["SERVICE_ACCOUNT_PATH"]

firebase_app = None


@dataclass(init=True, eq=True, order=True, unsafe_hash=False, frozen=False)
class FirebaseUser:
    uid: str
    email: str
    name: str

    @classmethod
    def from_user_record(cls, user_record: auth.UserRecord):
        return cls(user_record.uid, user_record.email, user_record.display_name)

    @classmethod
    def get_user_by_uid(cls, uid: str) -> "FirebaseUser":
        global firebase_app
        if firebase_app is None:
            raise FirebaseNotInitializedError()

        user_record = auth.get_user(uid)
        return cls.from_user_record(user_record)

    def __str__(self):
        return f"FirebaseUser(uid={self.uid}, email={self.email}, name={self.name})"

    def __repr__(self):
        return f"FirebaseUser({self.uid}, {self.email}, {self.name})"


def initialize_firebase() -> None:
    """
    Initializes the firebase app.
    """
    global firebase_app
    if firebase_app is not None:
        return

    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

    firebase_app = firebase_admin.initialize_app(cred)


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
