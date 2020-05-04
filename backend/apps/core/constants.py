# https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/#web-application-flow
# https://developers.google.com/identity/protocols/OpenIDConnect

OAUTH = {
    "github": {
        "name": "github",
        "url": "https://github.com/login/oauth/access_token",
    },
    "google-oauth2": {
        "name": "google-oauth2",
        "url": "https://oauth2.googleapis.com/token",
    },
    "facebook": {
        "name": "facebook",
        "url": "https://graph.facebook.com/v5.0/oauth/access_token",
    },
}

TEST_BASE_URL = "http://localhost"
