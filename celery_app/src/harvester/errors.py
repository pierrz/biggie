"""Module gathering all error classes"""
from abc import ABC


class ErrorBase(ABC, Exception):
    def __init__(self, error):
        self.info: str = error.__doc__


class GenericError(ErrorBase):
    """Hopefully helps notice new errors ..."""

    def __init__(self, error):
        super().__init__(error)
        print(
            f"/!\\ Error to investigate or specify better <- '{self.info}' - {type(error)}"
        )


class APILimitError(ErrorBase):
    """Specific to the API call, should show the missing key from the received data.
    Triggered by KeyError
    """

    def __init__(self, error):
        super().__init__(error)
        # TODO: print the missing key
        print(
            f"/!\\ The Github Events API limit is probably reached <- '{self.info}' - KeyError"
        )


class EmptyResults(ErrorBase):
    """Triggered by TypeError (due to None value)"""

    def __init__(self, error):
        super().__init__(error)
        print(
            f"/!\\ Empty results probably due to reaching the Github Events API limit <- '{self.info}' <- TypeError"
        )
