from logging.config import fileConfig

from alembic import context

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import Connection

from app.config import settings
from app.database.base import Base
from app.models.user import User


# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Add your model's MetaData object here
# for 'autogenerate' support.
#
# Importing User above is important because it makes sure
# the User model is registered in Base.metadata.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Offline mode configures Alembic with only a database URL
    and does not create an actual database connection.
    """

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Alembic runs inside the Docker API container, so the
    PostgreSQL service is reachable through the Docker hostname:
        postgres
    """

    database_url = settings.database_url

    # Convert the asyncpg driver used by the application
    # to the synchronous psycopg driver used by Alembic.
    database_url = database_url.replace(
        "postgresql+asyncpg://",
        "postgresql+psycopg://",
    )

    print(f"Alembic database URL: {database_url}")

    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine whether Alembic is running in offline or online mode.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()