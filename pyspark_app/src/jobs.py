"""
Spark jobs module
"""

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Iterable

# pylint: disable=E0611
from config import pyspark_config
from src.json_utils import load_json

from .mongo_connectors import CharacterReader, DataframeMaker


class SparkJobBase(ABC):
    """
    Base class to design actual job from
    """

    flag_files: bool    # to move the files once processed
    input_dir_path = pyspark_config.HARVESTER_OUTPUT_DIR
    input_array: Iterable[Dict]

    @abstractmethod
    def __init__(self):
        """
        Triggers the job sequence
        """

    @abstractmethod
    def get_input_array(self):
        """
        Gets the input data
        :return: does its thing
        """

    @abstractmethod
    def process_and_load_data(self):
        """
        Prepares and load data in Mongo
        :return: does its thing
        """


class SparkJobFromJson(SparkJobBase):
    """
    Job meant to process JSON files from a specific directory
    """

    def __init__(self):
        super().__init__()
        self.input_array = self.get_input_array()
        self.process_and_load_data()
        if self.flag:
            self.move_data()

    def get_input_array(self):

        input_array = []
        for file in os.scandir(self.input_dir_path):
            input_array += load_json(file)

        return input_array

    def process_and_load_data(self):
        try:
            print(f"{len(self.input_array)} rows available")
            DataframeMaker(
                self.input_array,
                "character",
                check_columns=["name", "comics_available"],
            ).load_mongo()
            CharacterReader()
            self.flag = True

        except Exception as exception:  # probably some Java error ...      # pylint: disable=W0703
            self.flag = False
            print("Error while executing the task ...")
            print(exception)

    def move_data(self):
        """
        Moves the processed files into the 'processed' directory
        :return: does its thing
        """
        for file in os.scandir(self.input_dir_path):
            shutil.move(file.path, Path(pyspark_config.PROCESSED_DIR, file.name))
