import os
from urllib import parse

import requests

from apps.core import constants as c


def get_payload(backend, code):

    # this might need a better solution
    key = f"{backend.upper()}_KEY".replace("-", "_")
    secret = f"{backend.upper()}_SECRET".replace("-", "_")

    client_id = os.environ.get(key, "nokey")
    client_secret = os.environ.get(secret, "nosecret")

    if backend == "github":
        payload = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

    # TODO: change `localhost` to env var
    elif backend == "google-oauth2":
        payload = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "http://localhost/auth/google-oauth2/callback",
            "grant_type": "authorization_code",
        }
    elif backend == "facebook":
        payload = {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": "http://localhost/auth/facebook/callback",
        }

    return payload


def get_access_token_from_code(backend, code):
    """Get access token for any OAuth backend from code"""

    url = c.OAUTH[backend]["url"]
    payload = get_payload(backend, code)

    # different providers have different responses to their oauth endpoints
    # for example:

    # github returns this:
    #
    #   b'access_token=76e9d25ed009fb7feroifjf0f58jf9rneb0b6b&scope=user&token_type=bearer'
    if backend == "github":
        r = requests.post(url, data=payload)

        # TODO: cleanup logic
        url = "http://example.com?" + str(r.content)
        params = dict(
            parse.parse_qsl(parse.urlsplit(url).query)
        )

        return params["b'access_token"]

    # google returns this:
    # {
    #   'access_token': 'ya29.frejf8erf.erferfeg.erfeogOS9tzAPQlNlUXitkMbmSt',
    #   'expires_in': 3596,
    #   'scope': 'openid https://www.googleapis.com/auth/userinfo.email',
    #   'token_type': 'Bearer',
    #   'id_token': 'oierfoie940j.ferferfoprek/refpekf9efoeik.long token'
    # }
    elif backend == "google-oauth2":
        r = requests.post(url, data=payload)

        token = r.json()["access_token"]

        return token

    elif backend == "facebook":
        r = requests.get(url, params=payload)
        token = r.json()["access_token"]
        return token
