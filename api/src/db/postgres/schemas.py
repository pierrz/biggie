from abc import ABC

from pydantic import BaseModel


class ORM(ABC, BaseModel):

    # allows the app to take ORM objects and translate them into responses automatically
    # (no more I/O wrangling e.g. ORM -> dict -> load)
    class Config:
        orm_mode = True


# class Record(ORM):
#     id: int
#     date: date
#     country: str


class Refugee(ORM):
    index: int
    data_date: str
    unix_timestamp: int
    individuals: int


class IDP(ORM):
    index: int
    IDPs: float
    Date: int
    source_url: str


class Country(ORM):
    index: int
    data_date: str
    unix_timestamp: int
    individuals: int
    origin_country: str
