from type import User
from db import execute


def get_user_by_id(user_id: str) -> User:
    result = execute("SELECT id, email, name FROM users WHERE id = %s", (user_id,))
    raw_user = result[0]

    if raw_user is None:
        pass

    return User(raw_user[0], raw_user[1], raw_user[2])

