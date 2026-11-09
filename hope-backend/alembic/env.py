from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# add your model's MetaData object here
# for 'autogenerate' support
from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.db import Base, get_database_url

target_metadata = Base.metadata
# URL comes from the environment, never from alembic.ini
config.set_main_option("sqlalchemy.url", get_database_url().replace("%", "%%"))

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def _migrate_connection(connection) -> None:
    from alembic.runtime.migration import MigrationContext
    from alembic.script import ScriptDirectory

    script = ScriptDirectory.from_config(config)
    known = {rev.revision for rev in script.walk_revisions()}
    current = set(MigrationContext.configure(connection).get_current_heads())
    unknown = current - known
    if unknown:
        raise RuntimeError(
            f"Database revision(s) {sorted(unknown)} are not present in this checkout. "
            "Deploy code containing those migrations before starting the service."
        )

    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # The runtime supplies its own connection so migrations use exactly the same
    # database as requests. Its caller owns the transaction and timeouts.
    connection = config.attributes.get("connection")
    if connection is not None:
        _migrate_connection(connection)
        return

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"connect_timeout": 10},
    )
    # The revision lookup itself starts a SQLAlchemy transaction. Own it before
    # that lookup so both the DDL and alembic_version are committed together.
    with connectable.begin() as connection:
        connection.exec_driver_sql("SET LOCAL lock_timeout = '5s'")
        connection.exec_driver_sql("SET LOCAL statement_timeout = '60s'")
        connection.exec_driver_sql("SELECT pg_advisory_xact_lock(719204631)")
        _migrate_connection(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
