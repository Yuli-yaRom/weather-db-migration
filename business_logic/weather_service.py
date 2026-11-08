# Бізнес-логіка: читання CSV і перетворення рядків у ORM-об'єкти
import pandas as pd

from data_access import repository
from data_access.models import Weather, WindDirection

CSV_COLUMNS = [
    "country", "location_name", "last_updated", "temperature_celsius", "condition_text", "sunrise",
    "wind_mph", "wind_kph", "wind_degree", "wind_direction", "gust_mph", "gust_kph",
]


def read_csv(path):
    df = pd.read_csv(path, usecols=CSV_COLUMNS)
    df["last_updated"] = pd.to_datetime(df["last_updated"])                       # "2024-05-16 13:15"
    df["sunrise"] = pd.to_datetime(df["sunrise"], format="%I:%M %p", errors="coerce").dt.time  # "05:42 AM"
    df = df.drop_duplicates(subset=["country", "location_name", "last_updated"])
    df = df.astype(object).where(df.notna(), None)                                # NaN -> None (NULL)
    return df.to_dict("records")


def parse_direction(text):
    if text in WindDirection.__members__:
        return WindDirection(text)
    return None


def import_csv(session, path):
    objects = []
    for row in read_csv(path):
        row["wind_direction"] = parse_direction(row["wind_direction"])
        objects.append(Weather(**row))
    repository.save_all(session, objects)
    return len(objects)
