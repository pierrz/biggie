"""
Test fixtures
"""

from datetime import datetime


class DataframeFixture:
    """
    Base class embeded with data to generate dataframes, eventually for specific collection
    """

    table_or_collection: str
    test_data = [
        {
            "a": 1,
            "b": 2.9,
            "c": "string1",
            "d": {"date": datetime(2000, 1, 1), "values": list(range(5))},
        },
        {
            "a": 2,
            "b": 3.9,
            "c": "string2",
            "d": {"date": datetime(2000, 2, 1), "values": list(range(7))},
        },
        {
            "a": 4,
            "b": 5.9,
            "c": "string3",
            "d": {"date": datetime(2000, 3, 1), "values": list(range(3))},
        },
    ]

    def __init__(self, table_or_collection):
        self.table_or_collection = table_or_collection
