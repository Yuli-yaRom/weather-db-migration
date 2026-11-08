# Підключення до баз даних
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_URLS = {
    "postgres": "postgresql+psycopg2://weather:weather@localhost:5432/weather",
    "mysql": "mysql+pymysql://weather:weather@localhost:3306/weather?charset=utf8mb4",
}


def get_engine(db_name="postgres"):
    return create_engine(DB_URLS[db_name])


def get_session(db_name="postgres"):
    return Session(get_engine(db_name))
