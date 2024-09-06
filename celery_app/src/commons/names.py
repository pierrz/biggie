from enum import Enum

# Logistics
filepath = "filepath"
data = "data"
mode = "mode"
output_keys = [filepath, data, mode]


# Github Event API
event = "event"


class CheckedColumns(str, Enum):
    event_id = f"{event}_id"
    type = "type"
    actor_id = "actor_id"
    repo_name = "repo_name"
