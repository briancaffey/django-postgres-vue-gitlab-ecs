import time

import celery

from celery.decorators import periodic_task
from celery.task import task
from celery.task.schedules import crontab


# http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance
class BaseTask(celery.Task):
    pass


@task(bind=True, base=BaseTask)
def debug_task(self):
    time.sleep(10)
    print("Task is done")
