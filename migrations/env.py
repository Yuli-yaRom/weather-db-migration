# Налаштування Alembic: до якої бази підключатись
from alembic import context
from sqlalchemy import create_engine

from data_access.database import DB_URLS
from data_access.models import Base

# alembic -x db=mysql upgrade head  -> беремо адресу MySQL; без -x -> Postgres
db_name = context.get_x_argument(as_dictionary=True).get("db", "postgres")
engine = create_engine(DB_URLS[db_name])

with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()
