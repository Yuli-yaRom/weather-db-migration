# Робота з базою даних: збереження і пошук записів
from data_access.models import Weather


def save_all(session, objects):
    session.add_all(objects)
    session.commit()


def count_weather(session):
    return session.query(Weather).count()
