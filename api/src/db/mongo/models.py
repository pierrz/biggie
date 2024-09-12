"""
Module dedicated to MongoDB models

TODO:
 - remove commented lines once update to Pydantic v2.x.x is fully functional/tested
 - investigate/implement the new field serializer
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, HttpUrl  # , field_serializer
from src.db.mongo.py_object_id import PyObjectId

# NB: When to use Field():
# - add extra validation, like Field(gt=0) for positive integers.
# - provide a description, like Field(description="The user's age")
# - specify an example value, like Field(example="John Doe")


class EventType(str, Enum):
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    WatchEvent = "WatchEvent"


class Event(BaseModel):
    """
    Container for a single event record.
    Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    """

    # The primary key for the Event model, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # id: Optional[str] = Field(default_factory=str, alias="_id")
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)

    event_id: int
    type: EventType
    public: str
    created_at: datetime
    actor_id: int
    actor_login: str
    actor_display_login: str
    # actor_gravatar_id could be int but it is always "" so far
    # actor_gravatar_id: Union[str, int]
    actor_gravatar_id: str
    actor_url: HttpUrl
    actor_avatar_url: HttpUrl
    repo_id: int
    repo_name: str
    repo_url: HttpUrl

    # @field_serializer("created_at")
    # def serialize_created_at(self, created_at: str, _info):
    #     return datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")

    # @field_serializer("ObjectId")
    # def serialize_created_at(self, ObjectId: PyObjectId, _info):
    #     return str(ObjectId)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        # json_encoders = {ObjectId: str, datetime: lambda v: v.isoformat()},
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "event_id": 12345,
                "type": "IssuesEvent",
                "public": True,
                "created_at": "2023-09-06T12:00:00Z",
                "actor_id": 67890,
                "actor_login": "username",
                "actor_display_login": "User Name",
                "actor_gravatar_id": "abcdef1234567890",
                "actor_url": "https://api.github.com/users/username",
                "actor_avatar_url": "https://avatars.githubusercontent.com/u/12345?v=4",
                "repo_id": 98765,
                "repo_name": "username/repo",
                "repo_url": "https://api.github.com/repos/username/repo",
            }
        },
    )


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

    repository_list: list[EventPerRepoCount]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "repository_list": [
                    {"name": "user/repo1", "count": 10},
                    {"name": "user/repo2", "count": 5},
                ]
            }
        }
    )


class EventTypeCount(BaseModel):
    """
    Model specific to count type occurences
    """

    type: EventType
    count: int


class EventTypeCountList(BaseModel):
    """
    Model specific to wrap the type occurence count results
    """

    count_per_type: list[EventTypeCount]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count_per_type": [
                    {"type": EventType.WatchEvent, "count": 10},
                    {"type": EventType.PullRequestEvent, "count": 5},
                ]
            }
        }
    )


class EventAverageTime(BaseModel):
    """
    Model specific to the calculation of the average time between PRs
    """

    pr_average_time_in_seconds: float
