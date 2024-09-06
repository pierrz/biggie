from datetime import datetime
from enum import Enum
from typing import List, Union

from bson import ObjectId
from pydantic import BaseModel, HttpUrl


class EventType(str, Enum):
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    WatchEvent = "WatchEvent"


class EventSchema(BaseModel):
    """
    Container for a single event record.
    Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    """
    id: int
    event_id: int
    type: EventType
    public: bool
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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }
        use_enum_values = True
        schema_extra = {
            "example": {
                "id": 1,
                "event_id": 12345,
                "type": "IssuesEvent",
                "public": True,
                "created_at": "2023-09-06T12:00:00Z",
                "org": "SomeOrg",
                "actor_id": 67890,
                "actor_login": "username",
                "actor_display_login": "User Name",
                "actor_gravatar_id": "abcdef1234567890",
                "actor_url": "https://api.github.com/users/username",
                "actor_avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
                "repo_id": 98765,
                "repo_name": "username/repo",
                "repo_url": "https://api.github.com/repos/username/repo"
            }
        }


class EventPerRepoCountSchema(BaseModel):
    """
    Model specific to count repo occurences
    """
    name: str
    count: int


class EventPerRepoCountListSchema(BaseModel):
    """
    Model specific to wrap the repo occurences count results
    """
    repository_list: List[EventPerRepoCountSchema]

    class Config:
        schema_extra = {
            "example": {
                "repository_list": [
                    {"name": "user/repo1", "count": 10},
                    {"name": "user/repo2", "count": 5}
                ]
            }
        }


# from abc import ABC
# from datetime import datetime
# from typing import Union

# from pydantic import BaseModel, HttpUrl

# from .models import EventType


# class ORM(ABC, BaseModel):

#     # allows the app to take ORM objects and translate them into responses automatically
#     # (no more I/O wrangling e.g. ORM -> dict -> load)
#     class Config:
#         orm_mode = True


# class Event(ORM):
#     """
#     Schema for a single event record.
#     Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
#     """

#     id: str
#     event_id: int
#     type: EventType
#     public: str
#     created_at: datetime
#     org: str
#     actor_id: int
#     actor_login: str
#     actor_display_login: str
#     actor_gravatar_id: Union[str, int]
#     actor_url: HttpUrl
#     actor_avatar_url: HttpUrl
#     repo_id: int
#     repo_name: str
#     repo_url: HttpUrl


# class EventPerRepoCount(ORM):
#     """
#     Schema specific to count repo occurences
#     """
#     name: str
#     count: int


# class EventPerRepoCountList(ORM):
#     """
#     Schema specific to wrap the repo occurences count results
#     """
#     repository_list: list[EventPerRepoCount]
