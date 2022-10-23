import psycopg2
from os import environ

DATABASE_HOST = environ["POSTGRES_HOST"]
DATABASE_USER = environ["POSTGRES_USER"]
DATABASE_PASSWORD = ["POSTGRES_PASSWORD"]
DATABASE_NAME = ["POSTGRES_DB_MAIN"]


def connect():
    return psycopg2.connect(
        host=DATABASE_HOST,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        dbname=DATABASE_NAME
    )

