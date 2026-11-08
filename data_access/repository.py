# Робота з базою даних: збереження і пошук записів
from datetime import datetime, timedelta

from sqlalchemy import func, select

from data_access.models import Weather


def save_all(session, objects):
    session.add_all(objects)
    session.commit()


def count_weather(session):
    return session.query(Weather).count()


def find_weather(session, country, day, location=None):
    """Записи для країни за один день. Регістр у назві країни/міста не важливий."""
    start = datetime(day.year, day.month, day.day)
    end = start + timedelta(days=1)
    query = (
        session.query(Weather)
        .filter(func.lower(Weather.country) == country.lower())
        .filter(Weather.last_updated >= start, Weather.last_updated < end)
    )
    if location:
        query = query.filter(func.lower(Weather.location_name) == location.lower())
    return query.order_by(Weather.location_name, Weather.last_updated).all()


def read_all_rows(engine, table):
    with engine.connect() as connection:
        return [dict(row) for row in connection.execute(select(table)).mappings()]


def insert_rows(engine, table, rows):
    with engine.begin() as connection:
        if rows:
            connection.execute(table.insert(), rows)


def count_rows(engine, table):
    with engine.connect() as connection:
        return connection.execute(select(func.count()).select_from(table)).scalar()
