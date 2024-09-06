from abc import ABC
from datetime import datetime
from typing import List

from pydantic import BaseModel


class ORM(ABC, BaseModel):

    # allows the app to take ORM objects and translate them into responses automatically
    # (no more I/O wrangling e.g. ORM -> dict -> load)
    class Config:
        orm_mode = True


class Event(ORM):
    """
    Container for a single event record.
    """
    id: int
    event_id: int
    type: str
    public: bool
    created_at: datetime
    org: str
    actor_id: int
    actor_login: str
    actor_display_login: str
    actor_gravatar_id: str
    actor_url: str
    actor_avatar_url: str
    repo_id: int
    repo_name: str
    repo_url: str

    class Config:
        use_enum_values = True


class EventPerRepoCount(ORM):
    """
    Model specific to count repo occurences
    """
    name: str
    count: int


class EventPerRepoCountList(ORM):
    """
    Model specific to wrap the repo occurences count results
    """
    repository_list: List[EventPerRepoCount]
