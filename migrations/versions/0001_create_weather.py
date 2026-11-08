"""Етап 1: створити таблицю weather

Revision ID: 0001
Revises:
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None

DIRECTIONS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
              "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]


def upgrade():
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("location_name", sa.String(100), nullable=False),
        sa.Column("last_updated", sa.DateTime, nullable=False),
        sa.Column("temperature_celsius", sa.Double),
        sa.Column("condition_text", sa.String(100)),
        sa.Column("sunrise", sa.Time),
        sa.Column("wind_mph", sa.Double),
        sa.Column("wind_kph", sa.Double),
        sa.Column("wind_degree", sa.Integer),
        sa.Column("wind_direction", sa.Enum(*DIRECTIONS, name="wind_direction_enum")),
        sa.Column("gust_mph", sa.Double),
        sa.Column("gust_kph", sa.Double),
    )


def downgrade():
    op.drop_table("weather")
    # у Postgres enum - це окремий тип, його треба видалити окремо (у MySQL нічого не станеться)
    sa.Enum(name="wind_direction_enum").drop(op.get_bind(), checkfirst=True)
