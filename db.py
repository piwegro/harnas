from typing import Optional, List, Tuple

import psycopg2
from os import environ

from exc import PostgresError


DATABASE_HOST = environ["POSTGRES_HOST"]
DATABASE_USER = environ["POSTGRES_USER"]
DATABASE_PASSWORD = environ["POSTGRES_PASSWORD"]
DATABASE_NAME = environ["POSTGRES_DB_MAIN"]

connection: Optional[psycopg2._psycopg.connection] = None


def connect() -> None:
    global connection
    if connection is not None:
        return

    try:
        connection = psycopg2.connect(
            host=DATABASE_HOST,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            dbname=DATABASE_NAME,
            options="-c search_path=piwegro"
        )
    except Exception as e:
        raise PostgresError(f"Error while connecting to Postgres: {e}")


def disconnect() -> None:
    """
    Disconnects from the database.

    :return: None
    """
    global connection
    if connection is None:
        return

    connection.close()
    connection = None


def fetch(query: str, params: tuple) -> List[Tuple]:
    """
    Fetches a single row from the database.

    :param query: SQL query to execute
    :param params: parameters to pass to the query

    :return: a list of tuples
    """

    try:
        global connection
        if connection is None:
            connect()
    except PostgresError:
        raise

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()

            return cursor.fetchall()
    except Exception as e:
        raise PostgresError(f"Error while fetching from Postgres: {e}")


def execute(query: str, params: tuple) -> None:
    """
    Executes a query on the database. Does not return anything.

    :param query: SQL query to execute
    :param params: parameters to pass to the query

    :return: None
    """
    try:
        global connection
        if connection is None:
            connect()
    except PostgresError:
        raise

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
    except Exception as e:
        raise PostgresError(f"Error while executing with Postgres: {e}")
