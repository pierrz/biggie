from enum import Enum

# Logistics
filepath = "filepath"
data = "data"
schema = "schema"
mode = "mode"
output_keys = [filepath, data, mode]


# DB: tables (PG) / collections (Mongo)
events = "events"


class CheckedColumns(str, Enum):
    event_id = "event_id"
    type = "type"
    actor_id = "actor_id"
    repo_name = "repo_name"
