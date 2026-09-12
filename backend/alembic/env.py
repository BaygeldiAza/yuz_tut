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

    Alembic is currently being executed from the host machine,
    while the database URL is configured for Docker.

    Docker uses:
        postgres

    The host machine needs:
        localhost

    Therefore, we convert the Docker hostname to localhost
    before creating the synchronous Alembic database engine.
    """

    # Start with the database URL from our application settings.
    database_url = settings.database_url

    # Convert the asyncpg driver to the synchronous psycopg driver.
    #
    # The application uses asyncpg, but Alembic's current
    # migration setup uses a synchronous SQLAlchemy engine.
    database_url = database_url.replace(
        "postgresql+asyncpg://",
        "postgresql+psycopg://",
    )

    # Convert the Docker PostgreSQL hostname to localhost.
    #
    # Inside Docker:
    #     postgres:5432
    #
    # From the host machine:
    #     localhost:5432
    database_url = database_url.replace(
        "@postgres:",
        "@localhost:",
    )

    # Print the final URL so we can verify that Alembic
    # is using the correct database connection.
    print(f"Alembic database URL: {database_url}")

    # Create the synchronous SQLAlchemy engine used by Alembic.
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    # Connect to PostgreSQL and run the migrations.
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