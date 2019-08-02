import os
from urllib import parse

import requests


def get_github_access_token_from_code(code):
    client_id = os.environ.get("GITHUB_KEY", "nokey")
    client_secret = os.environ.get("GITHUB_SECRET", "nosecret")

    url = "https://github.com/login/oauth/access_token"
    payload = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    r = requests.post(url, data=payload)

    url = "http://domain.com?" + str(r.content)
    params = dict(parse.parse_qsl(parse.urlsplit(url).query))
    return params["b'access_token"]
