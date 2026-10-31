
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# PostgreSQL connection URL
DATABASE_URL = (
    "postgresql+psycopg://postgres:YOUR_PASSWORD"
    "@localhost:5432/taskflow"
)

# Connect SQLAlchemy to PostgreSQL
engine = create_engine(DATABASE_URL)

# Create a factory for database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

# Base class for database models
class Base(DeclarativeBase):
    pass


# Provide a database session to each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
