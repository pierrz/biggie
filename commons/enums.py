"""
Module dedicated to all (potentially shared) Enum objects
"""

from enum import Enum


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
