import os
from urllib import parse

from core import constants as c

import requests


def get_payload(backend, code):


    key = f"{backend.upper()}_KEY"
    secret = f"{backend.upper()}_SECRET"

    client_id = os.environ.get(key, "nokey")
    client_secret = os.environ.get(secret, "nosecret")


    if backend == 'github':
        payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    elif backend == 'google_oauth2':
        payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': "http://localhost/auth/google/callback",
        'grant_type': "authorization_code"
    }

    return payload


def get_access_token_from_code(backend, code):
    """Get access token for any OAuth backend from code"""

    url = c.OAUTH[backend]['url']

    payload = get_payload(backend, code)

    r = requests.post(url, data=payload)

    # TODO: cleanup logic
    url = "http://example.com?" + str(r.content)
    params = dict(parse.parse_qsl(parse.urlsplit(url).query))

    return params["b'access_token"]
