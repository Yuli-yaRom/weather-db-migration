"""Етап 3: додати колонку should_go_outside ("Чи варто виходити на вулицю")

Revision ID: 0003
Revises: 0002

Три кроки:
  1) додаємо колонку, яка поки може бути пустою (NULL);
  2) заповнюємо її для всіх наявних рядків за формулою;
  3) робимо колонку обов'язковою (NOT NULL).
Значення за замовчуванням (DEFAULT) немає: для старих рядків ми рахуємо
справжнє значення, а для нових його рахує програма під час імпорту.
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"


def upgrade():
    # 1) нова колонка
    op.add_column("wind", sa.Column("should_go_outside", sa.Boolean, nullable=True))

    # 2) формула: вітер > 36 км/год (10 м/с) або пориви > 54 км/год (15 м/с) -> не виходити
    op.execute("""
        UPDATE wind
        SET should_go_outside = CASE
            WHEN wind_kph > 36 OR gust_kph > 54 THEN FALSE
            ELSE TRUE
        END
    """)

    # 3) тепер пустих значень немає -> колонка обов'язкова
    op.alter_column("wind", "should_go_outside", existing_type=sa.Boolean, nullable=False)


def downgrade():
    op.drop_column("wind", "should_go_outside")
