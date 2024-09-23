# from abc import ABC
from datetime import datetime
from test.sparky.base_test import PostgresTestReader
from typing import List

# from config import pyspark_config
from pydantic import BaseModel
from sqlalchemy import ARRAY, BigInteger, Column, DateTime, Float, String
from src.db.postgres_db import Base


class TestModel(BaseModel):
    """
    Model based on the Spark dataframe test fixture (Cf. 'mongo_schema.py')
    """

    a: int  # LongType() equivalent to 64-bit integer
    b: float  # DoubleType() equivalent to float
    c: str  # StringType() equivalent to string
    d_date: datetime  # TimestampType() equivalent to datetime
    d_values: List[int]  # ArrayType(LongType()) equivalent to list of integers


# class TableBase(ABC, Base):
#     table: str
#     __tablename__ = f"{pyspark_config.DB_USER}_schema.{table}"


# class TestTable(TableBase):
#     table = PostgresTestReader.table
class TestTable(Base):
    __tablename__ = PostgresTestReader.table

    id = Column(BigInteger, primary_key=True, autoincrement=True)  # Auto-incremented ID
    a = Column(BigInteger, nullable=True)  # Equivalent to LongType
    b = Column(Float, nullable=True)  # Equivalent to DoubleType
    c = Column(String, nullable=True)  # Equivalent to StringType
    d_date = Column(DateTime, nullable=True)  # Equivalent to TimestampType
    d_values = Column(
        ARRAY(BigInteger), nullable=True
    )  # Equivalent to ArrayType(LongType)
