import json
import os
import urllib.request

FULL_DOMAIN_NAME = os.environ.get("FULL_DOMAIN_NAME")
CELERY_METRICS_PATH = "api/celery-metrics/"

CELERY_METRICS_URL = f"https://{FULL_DOMAIN_NAME}/{CELERY_METRICS_PATH}"
CELERY_METRICS_TOKEN = os.environ.get("CELERY_METRICS_TOKEN")


def lambda_handler(event, context):
    data = {"celery_metrics_token": CELERY_METRICS_TOKEN}
    params = json.dumps(data).encode('utf8')
    req = urllib.request.Request(
        CELERY_METRICS_URL,
        data=params,
        headers={'content-type': 'application/json'},
    )
    response = urllib.request.urlopen(req)
    return response
