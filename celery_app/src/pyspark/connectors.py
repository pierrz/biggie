"""
Base connectors
"""

from abc import ABC, abstractmethod
from typing import Iterable, List, Tuple

# pylint: disable=E0611
from pyspark.sql import DataFrame
from pyspark.sql import functions as psf
from pyspark.sql.types import StructType


class ConnectorBase(ABC):
    check_columns: Iterable[psf.col]


class ReaderBase(ConnectorBase):
    """
    Base class dedicated to read data from a specific Mongo collection
    """

    db_data: DataFrame
    schema: StructType
    initial_id_col: List
    columns: Iterable[str]
    n_rows: int

    def preps_and_checks(self, db_data, check_columns=None):
        """
        Prepares the meta and generates the logs
        :param db_data: dataframe with data from the database
        """
        # preps
        self.n_rows = db_data.count()
        self.columns = list(db_data.columns)
        print("--> HERE5")
        print(self.columns)
        self.initial_id_col = self.columns[
            1
        ]  # hack to enforce ascending order (test purpose)
        self.db_data = db_data.sort(self.initial_id_col)
        self.schema = self.db_data.schema

        # checks
        print(self.__str__())
        if check_columns is None:
            self.db_data.select(*self.check_columns)
        else:
            self.db_data.select(*check_columns)
        print("--> HERE6")

    @abstractmethod
    def _name(self) -> Tuple[str]:
        """Get the right attribute name"""

    def __str__(self):

        trimmed_cols_str = ""
        for idx, column in enumerate([*self.columns[:3], "...", *self.columns[-3:]]):
            col_str = column
            if idx > 0:
                col_str = f", {col_str}"
            trimmed_cols_str += col_str

        name, element = self._name()[:2]
        return (
            f"Spark dataframe from {element} '{name}' "  # pylint: disable=E1101
            f"with {self.db_data.count()} rows and {len(self.columns)} columns [{trimmed_cols_str}]"
        )

    def __repr__(self):
        name, element, cls = self._name()
        # pylint: disable=E1101
        return f"{cls}('{name}' {element}, {len(self.columns)} columns, {self.db_data.count()} rows)"
