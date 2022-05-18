"""
Spark related Celery tasks
"""

import os
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Iterable

from config import app_config
from src.libs.main_lib import load_json
from src.spark.mongo_connectors import CharacterReader, DataframeMaker
# TODO: fully implement Celery logging (no more prints)
from worker import celery, logger


class SparkTaskBase(ABC):

    flag: bool
    dir_path = app_config.OUTPUT_DIR
    input_array: Iterable[Dict]

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_input_array(self):
        pass

    @abstractmethod
    def process_and_load_data(self):
        pass


class SparkTaskFromJson(SparkTaskBase):
    def __init__(self):
        self.input_array = self.get_input_array()
        self.process_and_load_data()
        if self.flag:
            self.move_data()

    def get_input_array(self):

        input_array = []
        for file in os.scandir(self.dir_path):
            array = load_json(file)
            input_array += array

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

        except Exception as e:  # probably some Java error ...
            self.flag = False
            logger.info("Error while executing the task ...")
            logger.info(e)

    def move_data(self):
        for file in os.scandir(self.dir_path):
            shutil.move(file.path, Path(app_config.PROCESSED_DIR, file.name))


@celery.task(name="spark_task")
def spark_task(previous_flag):

    if previous_flag:
        SparkTaskFromJson()
