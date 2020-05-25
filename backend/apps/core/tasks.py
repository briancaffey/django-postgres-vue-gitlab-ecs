import time

import celery
from celery.decorators import periodic_task
from celery.task import task
from celery.task.schedules import crontab
from django.core.mail import send_mail


# http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance
class BaseTask(celery.Task):
    pass


@task(bind=True, base=BaseTask)
def debug_task(self):
    time.sleep(10)
    print("Task is done")


@periodic_task(
    run_every=(crontab(minute="*/1")),
    name="debug_periodic_task",
    ignore_result=True,
)
def debug_periodic_task():
    print("Periodic task complete")


@task(bind=True, base=BaseTask)
def send_test_email_task(self):
    send_mail(
        "Subject here",
        "Here is the message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )


@task(bind=True, base=BaseTask)
def sleep_task(self, seconds):
    print("sleeping")
    time.sleep(int(seconds))
    return f"Slept {seconds} seconds"
