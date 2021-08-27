"""
This file has the module for generating Auth and Refresh token, respectively
"""

import datetime
import jwt
from django.conf import settings


def generate_auth_token(user):
    """
    Auth tokens carry the necessary information to access a resource directly.
    In other words, when a client passes an access token to a server managing
        a resource, that server can use the information contained in the token
        to decide whether the client is authorized or not.
    """

    # auth token payload which expires in 5 minutes
    auth_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() +
        datetime.timedelta(days=0, minutes=5),
        "iat": datetime.datetime.utcnow(),
    }
    # generating auth token using HS256 algorithm and then encoding it
    # with the jwt lib using the django secret key
    auth_token = jwt.encode(
        auth_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return auth_token


def generate_refresh_token(user):
    """
    The idea of refresh tokens is that if an access token is compromised,
    because it is short-lived, the attacker has a limited window to abuse it.

    Refresh tokens carry the information necessary to get a new access token.
    In other words, whenever an access token is required to access a specific
    resource, a client may use a refresh token to get a new access token issued
    by the authentication server.
    """

    # refresh token which expires in 5 days.
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() +
        datetime.timedelta(days=5),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )
    return refresh_token, refresh_token_payload['exp']
