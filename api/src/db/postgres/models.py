from enum import Enum
from typing import List

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EventType(str, Enum):
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    WatchEvent = "WatchEvent"


class Event(Base):
    """
    Container for a single event record.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)
    type = Column(SQLAlchemyEnum(EventType))
    public = Column(Boolean)
    created_at = Column(DateTime)
    org = Column(String)
    actor_id = Column(Integer)
    actor_login = Column(String)
    actor_display_login = Column(String)
    actor_gravatar_id = Column(String)
    actor_url = Column(String)
    actor_avatar_url = Column(String)
    repo_id = Column(Integer)
    repo_name = Column(String)
    repo_url = Column(String)


class EventPerRepoCount(BaseModel):
    """
    Model specific to count repo occurences
    """
    name: str
    count: int


class EventPerRepoCountList(BaseModel):
    """
    Model specific to wrap the repo occurences count results
    """
    repository_list: List[EventPerRepoCount]
