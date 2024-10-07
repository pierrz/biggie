"""
All postgres database related code
"""

from config import main_config
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST_DB = f"{main_config.POSTGRESDB_HOST}/{main_config.DB_NAME}"
POSTGRES_URI = f"postgresql://{main_config.POSTGRES_APP_USER}:{main_config.POSTGRES_APP_PASSWORD}@{HOST_DB}"

pg_engine = create_engine(POSTGRES_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
Base = declarative_base()
metadata = MetaData()


# Dependency
def get_db():
    """
    ensures that any route passed this function ought to have our SessionLocal database connection when needed
    and that the session is closed after use.
    """
    try:
        pg_db = SessionLocal()
        yield pg_db
    finally:
        pg_db.close()
