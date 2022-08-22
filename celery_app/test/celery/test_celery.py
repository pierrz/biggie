from test.tasks.test_task import dummy_task


# todo: transform it to check/init also Beat
def test_celery():
    """
    Just to check that Celery is up and running.
    """
    input = 3
    task = dummy_task.s(input)
    result = task()
    assert result == input**2
