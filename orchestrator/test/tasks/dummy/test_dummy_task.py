"""
Test that Celery and RabbitMQ are up and running.
"""

from src.tasks.dummy.dummy_task import dummy_task


# TODO: transform it to check/init also Beat
def test_celery():
    """
    Just to check that Celery is up and running.
    """
    input_value = 3
    task = dummy_task.s(input_value)
    result = task()
    assert result == input_value**2
