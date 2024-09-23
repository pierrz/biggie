"""
All postgres database related code
"""

import os

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host_db = (
    f"biggie_postgres:5432/{os.getenv('DB_NAME')}"  # with aggregated container name
)
connection_uri = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{host_db}"
)

pg_engine = create_engine(connection_uri)
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
