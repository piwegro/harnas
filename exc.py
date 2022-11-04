class FirebaseError (Exception):
    """Base class for all exceptions raised by the firebase module."""

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class FirebaseNotInitializedError (FirebaseError):
    """Raised when a function is called before firebase is initialized."""

    def __init__(self):
        super().__init__("Firebase is not initialized.")


class UserNotFoundError (Exception):
    """Raised when a user is not found in the database."""

    def __init__(self, uid):
        self.uid = uid

    def __str__(self):
        return f"User with uid {self.uid} not found."

