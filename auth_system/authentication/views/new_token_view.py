from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import views, exceptions
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from django.utils.decorators import method_decorator

from authentication.custom_auth.generate_token import (
    generate_auth_token)
import jwt

USER = get_user_model()


class RegenerateAuthToken(views.APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_protect)
    def get(self, request):
        """ To generate a new auth token the request expects:

        1. A cookie that contains a valid refresh_token
        2. A header 'X-CSRFTOKEN' with a valid csrf token
        """

        # getting refresh token from cookies, if there
        refresh_token = request.COOKIES.get('refreshToken')

        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            # decoding the payload to get the user details
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'Expired refresh token, please login again.')

        # confirming the user details from the DB
        user = USER.objects.filter(id=payload.get('user_id')).first()

        # validating the user
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        auth_token = generate_auth_token(user)
        return Response({'auth_token': auth_token})
