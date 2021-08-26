"""
Module for defining custom authentication
"""

import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

USER = get_user_model()


class CSRFCheck(CsrfViewMiddleware):

    def _reject(self, request, reason):
        return reason


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Decoding the user payload and authenticating user from the db
        """

        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            # getting the encoded auth_token, sperated by a space (' ')
            auth_token = authorization_header.split(" ")[1]

            # decoding the encoded payload to get user details
            payload = jwt.decode(
                auth_token, settings.SECRET_KEY, algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Access Token expired")

        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")

        # getting the user and checking for its presence
        user = USER.objects.filter(id=payload["user_id"]).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        self.enforce_csrf(request)
        return user, None

    def enforce_csrf(self, request):
        """
        Since django-rest-framwork enforces CSRF only in the
        session authentication, we need to ensure that it enforces CSRF
        for API views as well using the @ensure_csrf_cookie decorator
        """
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})

        if reason:
            raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)
