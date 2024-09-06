"""
Tests focused on Postgres based features
"""
from test.pyspark.base_test import PostgresDFTest, PostgresTestReader

from pandas.testing import assert_frame_equal
from src.db.postgres_db import pg_engine


class PostgresLoaderReaderTest(PostgresDFTest):
    """
    Test focused on the features of the PostgresLoader class
    """

    def run(self):

        test_df = self.data.spark_df
        self.data.load_postgres()
        postgres_df = PostgresTestReader().db_data

        # small hack to get the schemas right
        assert postgres_df.schema.simpleString() == test_df.schema.simpleString()
        assert_frame_equal(postgres_df.toPandas(), test_df.toPandas())


def test_postgres_loader_reader():
    """
    Starts the test
    :return: does its thing
    """

    PostgresLoaderReaderTest(PostgresTestReader.table)
    pg_engine.execute(f"DROP TABLE {PostgresTestReader.table}")
