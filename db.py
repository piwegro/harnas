import psycopg2
from os import environ

DATABASE_HOST = environ["POSTGRES_HOST"]
DATABASE_USER = environ["POSTGRES_USER"]
DATABASE_PASSWORD = environ["POSTGRES_PASSWORD"]
DATABASE_NAME = environ["POSTGRES_DB_MAIN"]

connection = None


def connect() -> None:
    global connection
    if connection is not None:
        return

    connection = psycopg2.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        dbname=DATABASE_NAME,
        options="-c search_path=piwegro"
    )


def fetch(query: str, params: tuple):
    """
    Fetches a single row from the database.

    :param query:
    :param params:
    :return:
    """
    global connection
    if connection is None:
        connect()

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()

        return cursor.fetchall()


def execute(query: str, params: tuple):
    """
    Executes a query on the database.

    :param query:
    :param params:
    :return:
    """
    global connection
    if connection is None:
        connect()

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        connection.commit()
