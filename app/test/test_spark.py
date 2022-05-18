import pandas as pd
from fastapi.testclient import TestClient
from pandas.testing import assert_frame_equal

from .base_test import DataframeTestBase

test_mongo_collection = "test_spark"


class DataframeMakerTest(DataframeTestBase):
    def run(self):

        assert (
            self.data.schema == self.fixture.test_schema
        )  # /!\ done before pd.json_normalize

        # data
        mapper = {}
        result_df = self.data.spark_df.toPandas()
        for col in result_df.columns.to_list():
            if "_" in col:
                mapper[col] = col.replace("_", ".")
        result_df.rename(columns=mapper, inplace=True)
        test_df = pd.json_normalize(self.fixture.test_data)

        assert_frame_equal(result_df, test_df)


def test_pyspark_dataframe_maker():
    DataframeMakerTest(test_mongo_collection)
