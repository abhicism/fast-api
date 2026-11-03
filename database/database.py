from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# SQLite keeps the API runnable without a separate database server.
DATABASE_URL = "sqlite:///./taskflow.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


def get_db():
    """Yield a database session for one request and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
