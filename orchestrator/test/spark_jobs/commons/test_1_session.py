import pytest
from src.spark_jobs.commons.session import session_check


def test_spark_session():
    """
    Test to check if a Spark session can be created and basic DataFrame operations work.
    """
    try:

        df = session_check()
        row_count = df.count()
        assert row_count == 3

        # Stop the Spark session
        # spark_session.stop()

    except Exception as e:
        pytest.fail(f"Spark session test failed: {e}")
