from abc import ABC
from datetime import datetime
from typing import Union

from pydantic import BaseModel, HttpUrl

from .models import EventType


class ORM(ABC, BaseModel):

    # allows the app to take ORM objects and translate them into responses automatically
    # (no more I/O wrangling e.g. ORM -> dict -> load)
    class Config:
        orm_mode = True


class Event(ORM):
    """
    Schema for a single event record.
    Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    """

    id: str
    event_id: int
    type: EventType
    public: str
    created_at: datetime
    org: str
    actor_id: int
    actor_login: str
    actor_display_login: str
    actor_gravatar_id: Union[str, int]
    actor_url: HttpUrl
    actor_avatar_url: HttpUrl
    repo_id: int
    repo_name: str
    repo_url: HttpUrl


class EventPerRepoCount(ORM):
    """
    Schema specific to count repo occurences
    """
    name: str
    count: int


class EventPerRepoCountList(ORM):
    """
    Schema specific to wrap the repo occurences count results
    """
    repository_list: list[EventPerRepoCount]
