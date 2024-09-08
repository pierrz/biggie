"""
Spark jobs module
TODO:
- align Mongo and Postgres jobs (table_or_collection)
- review/improve init inheritance structure
"""

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Tuple, Type, Union

from pyspark.sql.types import StructType
# pylint: disable=E0611
from src.utils.json_utils import load_json

from .dataframe_maker import MongoDataframeMaker, PostgresDataframeMaker


class SparkJobBase(ABC):
    """
    Base class to design actual job from
    :param flag_files: used to avoid moving unprocessed files too early
    :param input_dir_paths: list of input directories
    :param output_dir_path: ouput directory
    :param input_array: input data, as a list of data elements/records
    :param check_columns: which columns to print as workflow check
    :param reader_class: class used to read data loaded in Mongo
    :param custom_preps: if necessary, provide custom data preparations for the Dataframe Maker
    """

    flag_files: bool = False  # to move the files once processed
    input_dir_paths: Iterable[Path]
    output_dir_path: Path
    input_array: Iterable[Dict]
    check_columns: Iterable
    reader_class: Type
    schema: Optional[StructType]
    custom_preps: Optional[Union[Callable, Type]]

    def __init__(self, table_or_collection, check_columns, reader_class, custom_preps=None, schema=None):
        """
        Triggers the job sequence
        """
        self.table_or_collection = table_or_collection
        self.check_columns = check_columns
        self.reader_class = reader_class
        self.schema = schema
        self.custom_preps = custom_preps

    def get_input_array(self) -> Tuple[Iterable[Dict], int]:
        """
        Generate an array containing all new data as separate row per file
        :return: a JSON array and the count of invalid files
        """
        input_array = []
        invalid = 0
        for input_dir in self.input_dir_paths:
            for file in os.scandir(input_dir):
                data: List = load_json(file)

                if data is not None:
                    input_array += data  # /!\ not .append() as data is a list
                else:
                    invalid += 1

        return input_array, invalid

    @abstractmethod
    def process_and_load_data(self):
        """
        Prepares and load data in Mongo
        :return: does its thing
        """


class ToMongoFromJson(SparkJobBase):
    """
    Job meant to process JSON files from specific directories into Mongo
    and move them to an output directory
    """

    def __init__(
        self,
        input_dir_paths,
        collection,
        output_dir_path,
        check_columns,
        reader_class,
        custom_preps=None,
        schema=None
    ):
        super().__init__(collection, check_columns, reader_class, custom_preps, schema)
        self.input_dir_paths = input_dir_paths
        self.output_dir_path = output_dir_path
        json_array, invalid = self.get_input_array()

        if invalid > 0:
            print(f"There were {invalid} invalid or empty files.")

        if len(json_array) > 0:
            self.input_array = json_array
            self.process_and_load_data()
            if self.flag_files:
                self.move_data()
        else:
            print("No data to import.")

    def process_and_load_data(self):
        try:
            print(f"{len(self.input_array)} rows available")
            maker_parameters = {
                "input_array": self.input_array,
                "table_or_collection": self.table_or_collection,
                "check_columns": self.check_columns
            }
            print("--> HERE1")
            print(self.schema)
            if self.schema is not None:
                print("--> HERE2")
                maker_parameters["schema"] = self.schema
            if self.custom_preps is not None:
                maker_parameters["custom_preps"] = self.custom_preps
            # load, read afterwards and 'flag files' to move them
            MongoDataframeMaker(**maker_parameters).load_mongo()
            self.reader_class()
            self.flag_files = True

        except Exception as exception:  # probably some Java error ...      # pylint: disable=W0703
            print("Error while executing the task ...")
            print(exception)

    def move_data(self):
        """
        Moves the processed files into the 'processed' directory
        :return: does its thing
        """
        for input_dir in self.input_dir_paths:
            for file in os.scandir(input_dir):
                shutil.move(file.path, Path(self.output_dir_path, file.name))


class ToPostgresFromVA(SparkJobBase):
    """
    Job meant to process various files from specific directories into Postgres
    """

    def __init__(self, dataframe, table, check_columns, reader_class):
        super().__init__(table, check_columns, reader_class)

        if dataframe.size > 0:
            self.process_and_load_data(dataframe)
        else:
            print("No data to import.")

    def process_and_load_data(self, df):
        try:
            PostgresDataframeMaker(
                array_or_dataframe=df,
                table_or_collection=self.table_or_collection,
                check_columns=self.check_columns,
            ).load_postgres()

            self.reader_class(self.table_or_collection, self.check_columns)
            self.flag_files = True

        except Exception as exception:  # probably some Java error ...      # pylint: disable=W0703
            print("Error while executing the task ...")
            print(exception)
