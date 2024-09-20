import pytest

from sparky.src.session import spark_session


def test_spark_session():
    """
    Test to check if a Spark session can be created and basic DataFrame operations work.
    """
    try:

        # Simple DataFrame operation to test the connection
        data = [("Alice", 34), ("Bob", 45), ("Charlie", 29)]
        columns = ["Name", "Age"]
        df = spark_session.createDataFrame(data, columns)

        # Perform a simple DataFrame action (count)
        row_count = df.count()

        # Assert that the DataFrame has the expected number of rows
        assert row_count == 3

        # Stop the Spark session
        # spark_session.stop()

    except Exception as e:
        pytest.fail(f"Spark session test failed: {e}")
