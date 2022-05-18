"""
Test related Celery tasks
"""

import numpy as np
from src.spark.mongo_connectors import DataframeMaker
from src.tasks.spark_task import SparkTaskBase
from worker import celery, logger


@celery.task(name="init_check_task")
def init_check_task(*args):
    """
    [DEV PURPOSE] Checks whether Celery receives what is expected to
    :param args: some args
    :return: the 1st 2 args (why not ...)
    """
    logger.info("This comes in : %s", args)
    for arg_el in args:
        logger.info("- '%s'", arg_el)
    return args


@celery.task(name="dummy_task")
def dummy_task(input_int: int) -> int:
    """
    Dummy numpy task
    :param input_int: input number
    :return: list with input number & computed result
    """
    result = int(np.multiply(input_int, input_int))
    logger.info("=> Calculated: %s", result)

    return result


class SparkTaskTest(SparkTaskBase):
    def __init__(self, test_input_array):
        self.input_array = test_input_array
        self.process_and_load_data()

    def get_input_array(self):
        pass

    def process_and_load_data(self):
        try:
            print(f"{len(self.input_array)} rows available")
            DataframeMaker(
                self.input_array,
                "test_spark_celery",
                # self.collection,      # todo: potential refactorising
                check_columns=["a", "d_date"],
            ).load_mongo()
            self.flag = True

        except Exception as e:  # probably some Java error ...
            self.flag = False
            logger.info("Error while executing the task ...")
            logger.info(e)


@celery.task(name="spark_test")
def spark_test(test_data):
    flag = SparkTaskTest(test_data).flag
    return flag
