import time

import celery
from celery.decorators import periodic_task
from django.core.mail import send_mail

from backend.celery_app import app


# http://docs.celeryproject.org/en/latest/userguide/tasks.html#task-inheritance
class BaseTask(celery.Task):
    pass


@app.task(bind=True, base=BaseTask)
def debug_task(self):
    time.sleep(10)


@app.task(bind=True, base=BaseTask)
def debug_periodic_task():
    print("Periodic task complete")


@app.task(bind=True, base=BaseTask)
def send_test_email_task(self):
    send_mail(
        "Email subject",
        "Email message.",
        "from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )


@app.task(bind=True, base=BaseTask)
def sleep_task(self, seconds):
    time.sleep(int(seconds))
    return f"Slept {seconds} seconds"
