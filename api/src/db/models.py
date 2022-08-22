from sqlalchemy import Column, Float, Integer, String

from .postgres import Base


class Refugee(Base):
    __tablename__ = "refugees_view"

    index = Column(Integer, primary_key=True, index=True)
    data_date = Column(String(255))
    unix_timestamp = Column(Integer)
    individuals = Column(Integer)


class IDP(Base):
    __tablename__ = "idps_view"

    index = Column(Integer, primary_key=True, index=True)
    IDPs = Column(Float)
    Date = Column(Integer)
    source_url = Column(String(255), name="Source URL")


class Country(Base):
    __tablename__ = "countries_view"

    index = Column(Integer, primary_key=True, index=True)
    data_date = Column(String(255))
    unix_timestamp = Column(Integer)
    individuals = Column(Integer)
    origin_country = Column(String(255))
