"""Database engine/session setup. Credentials come from environment only."""
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    """INTERNAL url on Render (RENDER env var is set there), EXTERNAL locally.

    Falls back to a plain DATABASE_URL if the specific variables are absent.
    Normalised to the psycopg 3 SQLAlchemy driver.
    """
    on_render = bool(os.getenv("RENDER"))
    primary = "DATABASE_URL_INTERNAL" if on_render else "DATABASE_URL_EXTERNAL"
    url = os.getenv(primary) or os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(f"{primary} (or DATABASE_URL) is not set in the environment")
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
