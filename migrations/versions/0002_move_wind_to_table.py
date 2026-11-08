"""Етап 2: винести дані про вітер в окрему таблицю wind

Revision ID: 0002
Revises: 0001

Щоб не втратити дані, робимо у такому порядку:
  1) створюємо таблицю wind
  2) копіюємо в неї дані з weather
  3) тільки після цього видаляємо старі колонки з weather
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"

DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
              "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
WIND_COLUMNS = ["wind_mph", "wind_kph", "wind_degree", "wind_direction", "gust_mph", "gust_kph"]

# create_type=False: у Postgres тип wind_direction_enum вже створений у міграції 0001
direction_type = sa.Enum(*DIRECTIONS, name="wind_direction_enum", create_type=False)


def upgrade():
    # 1) нова таблиця
    op.create_table(
        "wind",
        sa.Column("weather_id", sa.Integer, sa.ForeignKey("weather.id"), primary_key=True),
        sa.Column("wind_mph", sa.Double),
        sa.Column("wind_kph", sa.Double),
        sa.Column("wind_degree", sa.Integer),
        sa.Column("wind_direction", direction_type),
        sa.Column("gust_mph", sa.Double),
        sa.Column("gust_kph", sa.Double),
    )
    # 2) копіюємо дані
    op.execute("""
        INSERT INTO wind (weather_id, wind_mph, wind_kph, wind_degree, wind_direction, gust_mph, gust_kph)
        SELECT id, wind_mph, wind_kph, wind_degree, wind_direction, gust_mph, gust_kph
        FROM weather
    """)
    # 3) видаляємо старі колонки
    for column in WIND_COLUMNS:
        op.drop_column("weather", column)


def downgrade():
    # повертаємо колонки в weather, копіюємо дані назад і видаляємо wind
    op.add_column("weather", sa.Column("wind_mph", sa.Double))
    op.add_column("weather", sa.Column("wind_kph", sa.Double))
    op.add_column("weather", sa.Column("wind_degree", sa.Integer))
    op.add_column("weather", sa.Column("wind_direction", direction_type))
    op.add_column("weather", sa.Column("gust_mph", sa.Double))
    op.add_column("weather", sa.Column("gust_kph", sa.Double))
    for column in WIND_COLUMNS:
        op.execute(f"UPDATE weather SET {column} = "
                   f"(SELECT {column} FROM wind WHERE wind.weather_id = weather.id)")
    op.drop_table("wind")
