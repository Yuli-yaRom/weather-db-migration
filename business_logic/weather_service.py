# Бізнес-логіка: читання CSV і перетворення рядків у ORM-об'єкти
import pandas as pd

from data_access import repository
from data_access.database import get_engine
from data_access.models import Weather, Wind, WindDirection

WEATHER_COLUMNS = ["country", "location_name", "last_updated", "temperature_celsius", "condition_text", "sunrise"]
WIND_COLUMNS = ["wind_mph", "wind_kph", "wind_degree", "wind_direction", "gust_mph", "gust_kph"]
CSV_COLUMNS = WEATHER_COLUMNS + WIND_COLUMNS


def read_csv(path):
    df = pd.read_csv(path, usecols=CSV_COLUMNS)
    df["last_updated"] = pd.to_datetime(df["last_updated"])                       # "2024-05-16 13:15"
    df["sunrise"] = pd.to_datetime(df["sunrise"], format="%I:%M %p", errors="coerce").dt.time  # "05:42 AM"
    df = df.drop_duplicates(subset=["country", "location_name", "last_updated"])
    df = df.astype(object).where(df.notna(), None)                                # NaN -> None (NULL)
    return df.to_dict("records")


def should_go_outside(wind_kph, gust_kph):
    """Чи варто виходити на вулицю.
    Ні - якщо вітер сильніший за 36 км/год (10 м/с) або пориви сильніші за 54 км/год (15 м/с)."""
    wind_kph = wind_kph or 0
    gust_kph = gust_kph or 0
    return wind_kph <= 36 and gust_kph <= 54


def parse_direction(text):
    if text in WindDirection.__members__:
        return WindDirection(text)
    return None


def import_csv(session, path):
    objects = []
    for row in read_csv(path):
        row["wind_direction"] = parse_direction(row["wind_direction"])
        weather = Weather(**{col: row[col] for col in WEATHER_COLUMNS})
        weather.wind = Wind(**{col: row[col] for col in WIND_COLUMNS})
        weather.wind.should_go_outside = should_go_outside(row["wind_kph"], row["gust_kph"])
        objects.append(weather)
    repository.save_all(session, objects)
    return len(objects)


def count_records(session):
    return repository.count_weather(session)


def find_weather(session, country, day, location=None):
    return repository.find_weather(session, country, day, location)


def copy_database(source_db="postgres", target_db="mysql"):
    """Копіює всі дані з однієї бази в іншу (id зберігаються).
    Перед цим у цільовій базі треба виконати ті самі міграції:  alembic -x db=mysql upgrade head"""
    source = get_engine(source_db)
    target = get_engine(target_db)
    tables = [Weather.__table__, Wind.__table__]   # спочатку weather, бо wind посилається на неї

    for table in tables:
        if repository.count_rows(target, table) > 0:
            return f"Помилка: у {target_db} таблиця {table.name} вже не порожня"

    report = []
    for table in tables:
        rows = repository.read_all_rows(source, table)
        repository.insert_rows(target, table, rows)
        report.append(f"{table.name}: {source_db} = {repository.count_rows(source, table)}, "
                      f"{target_db} = {repository.count_rows(target, table)}")
    return "\n".join(report)
