# Celery and Redis

Let's create a new branch called `feature-celery` where we will add Celery to our application. Adding Celery and Redis will allow us to process tasks asynchronously.

## Adding Celery and Redis
To add celery to our project we will need to do the following:

- Add `celery` and `redis` services to our docker-compose files
- Add `celery` and `redis` to our `requirements.txt`
- Add `celery` settings in `settings.py`
- Add `celery_app.py` to our Django application
- Test `celery` and `redis` with a sample task

### Docker Compose

Add the following to both `docker-compose.yml` and `docker-compose.dev.yml`:

```yml
  redis:
    image: redis:alpine
    container_name: redis
    networks:
      - main

  celery:
    build: ./backend
    container_name: celery
    command: bash -c 'celery worker --app=backend.celery_app:app --loglevel=info'
    volumes:
      - ./backend:/code
    depends_on:
      - db
      - redis
    networks:
      - main
```

Now add the following to `requirements.txt`:

```
celery==4.2
redis==2.10.5
```

Add the following to our Django settings (`settings.py`):

```python
# Celery Configuration

CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
```

### Define our Celery App

Now add `celery_app.py` next to `settings.py` in Django:

```python
import os
from celery import Celery
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Doing async task")
    time.sleep(2)
    print("Task is done")
```

Additionally, we need to add two lines of code to `backend/__init__.py` that will allow us to register Celery tasks in all of our Django apps:

**backend/backend/__init__.py**

```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

### Sample Task

Let's test that this sample task is processed in our celery worker. In the `posts` app, let's add a function and map it to a url pattern. We will call the task inside the function body:

**backend/posts/views.py**

```python
from backend.celery_app import debug_task

from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

...

@api_view()
@authentication_classes([])
@permission_classes([])
def celery_test_view(request):
    debug_task.delay()
    return Response({"message": "Your task is being processed!"})
```

**backend/posts/urls.py**

```python
from django.urls import path

from . import views

urlpatterns = [
    ...
    path('celery-test/', views.celery_test_view, name='celery-test')
]
```

Now let's test this sample task. Run:

```
docker-compose -f docker-compose.dev.yml up --build
```

Now navigate to `/api/posts/celery-test/`. You should see the JSON response returned right away, and two seconds later you should see the `"Task is done"` message printed out in the `celery` service logs. Also verify that celery tasks are working in the production environment:

```
docker-compose up --build
```

### Auto-refresh Celery

Let' make on more optimization for our development environment as it relates to celery. If you have worked with Celery and Django before, you know that making changes to celery requires that celery is restarted. We can add a Django management command that will restart celery when changes to our `backend` codebase are saved.

Django managment commands should be put in Django apps. Let's make a new Django app called `core` following the same steps we took while creating our `posts` app. `core` will serve as an app to put things that are not directly related to any other app logic.

Next, let's add a file called `watch_celery.py`:

*`backend/core/management/commands/watch_celery.py`*:

```python
"""
This command allows for celery to be reloaded when project
code is saved. This command is called in
`docker-compose.dev.yml` and is only for use in development

https://avilpage.com/2017/05/how-to-auto-reload-celery-workers-in-development.html
"""

import shlex
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill -9 celery'
    subprocess.call(shlex.split(cmd))
    cmd = 'celery worker --app=backend.celery_app:app --loglevel=info'
    subprocess.call(shlex.split(cmd))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.main(restart_celery)
```

Now let's change the `command` part of the `celery` service in `docker-compose.dev.yml`:

```yml
    command: bash -c 'python3 manage.py watch_celery'
```

We can verify that this works by changing the text returned by our `celery-test-view` function, and we can also see that the celery service is restarted when we save change changes to our `backend` code.

We will not change the `celery` `command` for `docker-compose.yml`, because we won't be editing code in our production app.

### Flower

Let's add one more container that will help us monitor Celery tasks: `flower`.

Add the following to both `docker-compose.yml` and `docker-compose.dev.yml`:

```yml
  flower:
    image: mher/flower
    container_name: flower_dev_vet
    command: flower --url_prefix=flower
    environment:
      - CELERY_BROKER_URL=redis://redis:6379
      - FLOWER_PORT=5555
    ports:
      - 5555:5555
    networks:
      - main
    depends_on:
      - celery
      - redis
```

And then add the following to `dev.conf` and `prod.conf` NGINX configurtion files:

```
  upstream flower {
    server flower:5555;
  }

...

    # flower
    location /flower/ {
        rewrite ^/flower/(.*)$ /$1 break;
        proxy_pass http://flower/;
        proxy_set_header Host $host;
        proxy_redirect off;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
```

Once we have verified that tasks are also working for our production environment and that we can view the flower dashboard when we visit `/flower` in the browser, let's commit our changes and make a new minor release for our new celery feature.

```
git add .
git commit -m "added celery and redis"
git checkout develop
git merge feature-celery
git checkout -b release-0.0.5
git checkout master
git merge release-0.0.5
git tag -a 0.0.5
git push --all
git push --tags
```
