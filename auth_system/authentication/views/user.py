"""
This file has the module for user Login and SignUp
"""

from authentication.custom_auth.generate_token import (
    generate_auth_token, generate_refresh_token)
from authentication.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import views, status, exceptions
from rest_framework.response import Response

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny

USER = get_user_model()


class UserSignUp(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        This module wil handle user's registration
        """
        data = request.data

        user = USER.objects.filter(email=data['email'])
        if user.exists():
            return Response('User already exists. Login to contine',
                            status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('SignUp successfull. Please login to continue')


class UserLogin(views.APIView):
    permission_classes = [AllowAny]

    @ensure_csrf_cookie
    def post(self, request):
        """
        Module for allowing user to login
        """

        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()

        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'Email and password required')

        user = USER.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')

        serializer_user = UserSerializer(user).data

        # generating access token and refresh token
        auth_token = generate_auth_token(user=user)
        refresh_token = generate_refresh_token(user=user)

        # storing the cookie in the response
        response.set_cookie(key='refreshToken',
                            value=refresh_token, httponly=True)
        response.data = {'auth_token': auth_token, 'user': serializer_user}
        return response
