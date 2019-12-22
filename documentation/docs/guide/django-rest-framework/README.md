---
footer: MIT Licensed | Copyright © 2018-present Brian Caffey
---

# Backend API

At this point, we are going to add some additional packages to Django that will allow us to build a powerful API.

## Overview

When I say that we will build an API with Django, what I mean is that we will establish a structured set of URLS that we will return responses when we make HTTP requests to these URLs. Before we look at an example of what this means, it is important to know that HTTP requests are split into different types by their method. Here are the different types of HTTP requests methods:

- `GET`: The GET method requests a representation of the specified resource. Requests using GET should only retrieve data.
- `HEAD`: The HEAD method asks for a response identical to that of a GET request, but without the response body.
- `POST`: The POST method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
- `PUT`: The PUT method replaces all current representations of the target resource with the request payload.
- `DELETE`: The DELETE method deletes the specified resource.
- `CONNECT`: The CONNECT method establishes a tunnel to the server identified by the target resource.
- `OPTIONS`: The OPTIONS method is used to describe the communication options for the target resource.
- `TRACE`: The TRACE method performs a message loop-back test along the path to the target resource.
- `PATCH`: The PATCH method is used to apply partial modifications to a resource.

We will mostly be using `GET`, `POST`, `DELETE`, `PUT` and `PATCH`. These methods correspond to the actions of a `CRUD` app: `create`, `read`, `update`, `delete`.

- `POST` is similar to `create`
- `GET` is similar to `read`
- `PUT` and `PATCH` are similar to `update`
- `DELETE` is similar to `delete`

Now let's look at a basic example. Let's say our app allows users to read, write, update and delete blog posts.

When a user reads a blog post, we will be accessing data through one of our API's endpoints. Accessing the data will involve an HTTP request that will use a `GET` *HTTP requests method*. For example:

We make a `GET` request to `https://www.our-site.com/api/posts/3/`. The Django ReST Framework will process this requests, fetch a post with an `id` of `3`, and return this post in JSON form. It might look something like this:

```json
{
    "id": 3,
    "title": "My Third Post",
    "content": "Today I wrote my third blog post, ...",
    "draft": false,
    "publish_date": "2050-03-08",
}
```

### Django ReST Framework

The [Django ReST Framework](https://www.django-rest-framework.org/) will be responsible for serializing and deserializing our Django models instances (which are python objects) to and from JSON.

It has many powerful features that make it the most popular package for building APIs with Django. Here are some additional features that we will use later:

- `Permissions`: how do we control what users can access what resources.
- `Pagination`: Let's say we have millions of posts and the user wants to browse all of the posts. We will want to send the user one set of posts and let the user click through a list of pages to see more posts. Each time the user clicks on a new page, we make a new get request to the ReST API.

In addition to the Django ReST Framework, we will install another package for using JSON Web Tokens for authentication and permission control. This package is called [`djangorestframework_jwt`](https://github.com/GetBlimp/django-rest-framework-jwt) and it is maintained by a company called [Blimp](https://github.com/GetBlimp).

Before we start, let's go back to the `feature-django` branch to continue our work with the backend Django service:

```
git checkout feature-django
```

### DRF Installation

First let's add these packages to `requirements.txt`:

```python
djangorestframework
django-filter
djangorestframework-jwt
```

Next, we will need to add the following to `INSTALLED_APPS`:

```python

    'rest_framework',

```

Then we can add the following to `settings.py` after `DATABASES`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```

This defines default behavior for our Django ReST Framework views. If a user tries to access a post (for example, the user makes a request to `/api/posts/1/`), we check the `DEFAULT_PERMISSION_CLASSES`. This is a tuple of permission classes, and there is only one in the settings we have defined above: `'rest_framework.permissions.IsAuthenticated'`. This checks if a user is authenticated or not. To check if a user is authenticated or not, we check `'DEFAULT_AUTHENTICATION_CLASSES'`. This is also a tuple. We will check the the three values `JSONWebTokenAuthentication`, `SessionAuthentication` and `BasicAuthentication`, one at a time. As soon as one of these classes says that the user is authenticated, we stop checking, and it is determined that the user is authenticated. If it is determined that a user is authenticated, then the user has permission to access the resource in question (`/api/posts/1/`, for example).

We have a little bit more work to do on the backend. Once we build out an authentication system and a basic model like "Blog Posts", we will be ready to set up a user interface that will to login and also get and post data to our backend Django API. Then we will tie the backend and the frontend together with a powerful webserver and reverse proxy: NGINX.

## User Authentication

First, we need a new Django app to organize our project's users. Let's create a new app called `accounts`. We will need to issue a `startapp` command to the `backend` container, change permissions on those files, and then add the name of the app to `INSTALLED_APPS` so our project becomes aware of it. We will also need to create API endpoints. Let's do this all step-by-step.

First, let's make the app:

```
docker exec -it backend python3 backend/manage.py startapp accounts
```

Set permissions on the files in the `accounts` app:

```
sudo chown -R $USER:$USER .
```

Move the app to be inside the Django project:

```
mv accounts/ backend/
```

### URL Routing

Now let's hook up our `accounts` app to the rest of our Django project. Add `'accounts'` to `INSTALLED_APPS` and add the following to the `urls.py` file in `backend`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
```

Add `urls.py` to `accounts` and add the following:

Now, to the `urls.py` file in the `accounts` app, add the following:

```python
from django.urls import re_path
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

urlpatterns = [
    re_path(
        r'^auth/obtain_token/',
        obtain_jwt_token,
        name='api-jwt-auth'
    ),
    re_path(
        r'^auth/refresh_token/',
        refresh_jwt_token,
        name='api-jwt-refresh'
    ),
    re_path(
        r'^auth/verify_token/',
        verify_jwt_token,
        name='api-jwt-verify'
    ),
]
```

The first route will return a JSON response containing a special token when we send a POST request with the correct `username` and `password`. Actually, `djangorestframework_jwt` supports `AbstractBaseUser`, so we should be able to authenticate with any combination of credentials, but we will only be looking at the standard user model for now.

Let's write a test to see how this works in action. In `accounts/tests.py`, add the following:

```python
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


from django.contrib.auth.models import User

class TestAccounts(APITestCase):

    def test_obtain_jwt(self):

        # create an inactive user
        url = reverse('api-jwt-auth')
        u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        u.is_active = False
        u.save()

        # authenticate with username and password
        resp = self.client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # set the user to activate and attempt to get a token from login
        u.is_active = True
        u.save()
        resp = self.client.post(url, {'username':'user', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        # print the token
        print(token)
```

We can run this test like this:

```
docker exec -it backend python3 backend/manage.py test accounts
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InVzZXIiLCJleHAiOjE1NDA2ODg4MjMsImVtYWlsIjoidXNlckBmb28uY29tIn0.9nXmNoF0dX-N5yh33AXX6swT5zDchosNI0-bcsdSUEk
.
----------------------------------------------------------------------
Ran 1 test in 0.173s

OK
Destroying test database for alias 'default'...
```

### JSON Web Tokens

Our test passes, and we can see the JWT printed out at the end of the test. Here's a JWT, decoded:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM4MzMwNTk5LCJlbWFpbCI6IiJ9.rIHFjBmbqBHnqKwCNlHenImMtQSmzFkbGLA8pddQ6AY
```

Decoded, this JWT contains two JSON objects and a signature:

```json
{"typ":"JWT","alg":"HS256"}{"user_id":2,"username":"admin","exp":1538330599,"email":""}Ō稬6QޜY<P
```

The first part of JSON identifies the type of token and the hashing algorithm used. The second part is a JSON representation of the authenticated user, with additional information about when the token expires. The third part is a signature that uses the `SECRET_KEY` of our Django application for security.

We can also try this endpoint in the Django ReST Framework's browseable API by going to `http://0.0.0.0:8000/auth/obtain_token/`. You will see this:

```
HTTP 405 Method Not Allowed
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Method \"GET\" not allowed."
}
```

This makes sense, because this endpoint only accepts POST requests. From the browseable API, we can make a POST request using our superuser account. Below this message, you will see a form that allows us to enter a username and password.

Let's create a superuser and do a quick check that this is working inside of the browsable API:

```
docker exec -it backend python3 backend/manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address:
Password:
Password (again):
Superuser created successfully.
```

Entering our username and password for the user we created in the browsable API login form, we can see that a token is return in the respsonse body.


## Sample Model

Now that we have a working user authentication system, let's create a simple "Blog Post" model in a new app called `posts`. I'm going to borrow code from [this Django Rest Framework tutorial](https://wsvincent.com/django-rest-framework-tutorial/).

Create a `posts` app in our Django project through `docker exec` as we did before:

```
docker exec -it backend python3 backend/manage.py startapp posts
sudo chown -R $USER:$USER .
mv posts/ backend/
```

Next, add `posts` to `INSTALLED_APPS`, and link up the urls in `backend` with:

**backend/backend/urls.py**

```python
urlpatterns = [
  ...
  path('api/posts/', include('posts.urls')),
]
```

### Defining the Model

Now we can add the model:

**backend/posts/models.py**

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```
### Model Registration for Django Admin

Next let's register this app with the Django admin:

**backend/posts/admin.py**

```python
from django.contrib import admin
from . models import Post

admin.site.register(Post)
```

### Model Serializer

Then add a serializer for this model by creating `serializers.py` in the `posts` folder:

**backend/posts/serializers.py**

```python
from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'content', 'created_at', 'updated_at',)
        model = models.Post

```

We will need to add `urls.py` to `posts` with the following:

**backend/posts/urls.py**

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='posts'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
]
```

Finally, we will add two views that we mapped to endpoints in the code above:

**backend/posts/views.py**

```python
from rest_framework import generics

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

Now, let's add some Post objects in the Django admin. Before we do this, we will need to make migrations run the migrations:

```
docker exec -it backend python3 backend/manage.py makemigrations
Migrations for 'posts':
  backend/posts/migrations/0001_initial.py
    - Create model Post
```

And then run migrations:

```
docker exec -it backend python3 backend/manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, posts, sessions
Running migrations:
  Applying posts.0001_initial... OK
```

Now we can add some `Post` objects.

### DRF Settings

Go back to the browsable api and visit `/api/posts/`. You should see the posts you created in admin.

Earlier we configured `REST_FRAMEWORK` in `backend/backend/settings.py`. Let's see what happens when we remove session and basic authentication:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}
```

Now, when we visit `/api/posts/` again, we should see:

```json
HTTP 401 Unauthorized
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
WWW-Authenticate: JWT realm="api"

{
    "detail": "Authentication credentials were not provided."
}
```

Let's restore the original settings for `REST_FRAMEWORK` for now, but remove `BasicAuthentication`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}
```

### Testing our Model

Before we start working on our frontend, let's write some tests to make sure that access to our posts is limited to requests that come with a valid token.

**posts/tests.py**

```python
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from rest_framework_jwt.settings import api_settings


class TestPosts(TestCase):
    """Post Tests"""

    def test_get_posts(self):
        """
        Unauthenticated users should not be able to access posts via APIListView
        """
        url = reverse('posts')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_header_for_token_verification(self):
        """
        https://stackoverflow.com/questions/47576635/django-rest-framework-jwt-unit-test
        Tests that users can access posts with JWT tokens
        """

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        user.is_active = True
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        verify_url = reverse('api-jwt-verify')
        credentials = {
            'token': token
        }

        resp = self.client.post(verify_url, credentials, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
```

Let's add a `.flake8` file to `/backend` so that flake8 will ignore migration files:

**backend/.flake8***

```
[flake8]
exclude =
    */migrations/*
```

More information on configuring flake8 can be found [here](http://flake8.pycqa.org/en/3.1.1/user/configuration.html).

Let's commit our changes:

```
git add .
git commit -m "added posts model, permission tests for post model"
git push
```

Our automated tests are passing. Let's merge these changes into the `develop` branch. We will leave our `backend` service for now and start working on the frontend of our application.

```
git checkout develop
git merge feature-django
git checkout -b release-0.0.2 develop
git checkout master
git merge release-0.0.2
git tag -a 0.0.2
git push --all --tags
```
