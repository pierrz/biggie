"""
Tests focused on Postgres based features
"""

from test.spark_jobs.utils.base_test import PostgresDFTest, PostgresTestReader

from pandas.testing import assert_frame_equal
from sqlalchemy import Table
from src.db.postgres.postgres_db import metadata, pg_engine


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

    test_table = PostgresTestReader.table
    PostgresLoaderReaderTest(test_table)

    # db cleaning
    table_to_drop = Table(test_table, metadata, autoload_with=pg_engine)
    with pg_engine.begin() as context:
        table_to_drop.drop(context)
