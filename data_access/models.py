# ORM-модель бази даних (SQLAlchemy).
# Описуємо не всі колонки CSV, а тільки ті, що нам потрібні.
import enum

from sqlalchemy import Column, DateTime, Double, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class WindDirection(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)            # текст
    location_name = Column(String(100), nullable=False)
    last_updated = Column(DateTime, nullable=False)          # дата
    temperature_celsius = Column(Double)
    condition_text = Column(String(100))
    sunrise = Column(Time)                                   # час

    # дані про вітер лежать в окремій таблиці (зв'язок один-до-одного)
    wind = relationship("Wind", back_populates="weather", uselist=False)


class Wind(Base):
    # категорія "вітер" (варіант 17 -> 17 mod 4 = 1)
    __tablename__ = "wind"

    weather_id = Column(Integer, ForeignKey("weather.id"), primary_key=True)
    wind_mph = Column(Double)
    wind_kph = Column(Double)                                # дробне число
    wind_degree = Column(Integer)                            # ціле число
    wind_direction = Column(Enum(WindDirection, name="wind_direction_enum"))  # enumeration
    gust_mph = Column(Double)
    gust_kph = Column(Double)

    weather = relationship("Weather", back_populates="wind")
