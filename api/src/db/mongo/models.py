# from src.db.mongo.py_object_id import PyObjectId
from datetime import datetime
from enum import Enum
from typing import Union

from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl


class EventType(str, Enum):
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    WatchEvent = "WatchEvent"


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Event(BaseModel):
    """
    Container for a single event record.
    Cf. https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    # id: Optional[str] = Field(default_factory=str, alias="_id")

    # The primary key for the EventModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)

    event_id: int = Field()
    type: EventType
    public: str = Field()
    created_at: datetime = Field()
    org: str = Field()
    actor_id: int = Field()
    actor_login: str = Field()
    actor_display_login: str = Field()
    actor_gravatar_id: Union[str, int] = Field()
    actor_url: HttpUrl = Field()
    actor_avatar_url: HttpUrl = Field()
    repo_id: int = Field()
    repo_name: str = Field()
    repo_url: HttpUrl = Field()

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str
        }
        use_enum_values = True

    # Pydantic > v2.x.x
    # model_config = ConfigDict(
    #     populate_by_name=True,
    #     arbitrary_types_allowed=True,
    #     # json_schema_extra={
    #     #     "example": {
    #     #         "name": "Jane Doe",
    #     #         "email": "jdoe@example.com",
    #     #         "course": "Experiments, Science, and Fashion in Nanophotonics",
    #     #         "gpa": 3.0,
    #     #     }
    #     # },
    #     json_encoders = {
    #         datetime: lambda v: v.isoformat()
    #     }
    # )


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
