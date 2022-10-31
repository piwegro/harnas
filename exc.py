class FirebaseError (Exception):
    """Base class for all exceptions raised by the firebase module.

    Attributes:
        message: A string describing the error.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class FirebaseNotInitializedError (FirebaseError):
    """Raised when a function is called before firebase is initialized."""

    def __init__(self):
        super().__init__("Firebase is not initialized.")
