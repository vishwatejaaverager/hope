"""Apply committed schema migrations to the application's database at startup."""
import logging
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine

logger = logging.getLogger('uvicorn.error')


def upgrade_database(engine: Engine) -> None:
    config = Config(str(Path(__file__).resolve().parent.parent / 'alembic.ini'))
    logger.info('Applying database migrations before accepting requests')
    try:
        with engine.begin() as connection:
            # Bound queries/locks and serialize simultaneous service starts.
            connection.exec_driver_sql("SET LOCAL lock_timeout = '5s'")
            connection.exec_driver_sql("SET LOCAL statement_timeout = '60s'")
            connection.exec_driver_sql('SELECT pg_advisory_xact_lock(719204631)')
            config.attributes['connection'] = connection
            command.upgrade(config, 'head')
    except Exception:
        logger.exception('Database migration failed; refusing to start with an incompatible schema')
        raise
    logger.info('Database migrations committed successfully')
