from enum import Enum

# Logistics
filepath = "filepath"
data = "data"
diagrams = "diagrams"
schema = "schema"
mode = "mode"
received = "received"
processed = "processed"
output_keys = [filepath, data, mode]


# DB: tables (PG) / collections (Mongo)
events = "events"
created_at = "created_at"


class ValueEnum(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)


class CheckedColumns(ValueEnum):
    event_id = "event_id"
    type = "type"
    actor_id = "actor_id"
    repo_name = "repo_name"


class GithubEventTypes(ValueEnum):
    IssuesEvent = "IssuesEvent"
    PullRequestEvent = "PullRequestEvent"
    WatchEvent = "WatchEvent"
