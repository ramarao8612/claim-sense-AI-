"""SQLAlchemy engine + session. One place creates the DB connection;
routers import SessionLocal / get_db from here."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import models so Base.metadata knows every table, then create them.
    from app import models  # noqa: F401

    from pgvector.sqlalchemy import Vector  # noqa: F401  (registers type)

    with engine.begin() as conn:
        conn.execute(__import__("sqlalchemy").text("CREATE EXTENSION IF NOT EXISTS vector"))
    Base.metadata.create_all(bind=engine)
