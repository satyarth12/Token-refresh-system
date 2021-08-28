"""
This file has the module for user SignUp, user Login
and getting user details, in respective order.
"""

from django.utils.decorators import method_decorator
from authentication.custom_auth.generate_token import (
    generate_auth_token, generate_refresh_token)
from authentication.serializers import UserSerializer

from django.contrib.auth import get_user_model
from rest_framework import views, status, exceptions, generics
from rest_framework.response import Response

from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

USER = get_user_model()


class UserSignUp(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

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
    serializer_class = UserSerializer

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ))
    # ensure_csrf_cookie Enforces DRF to send CSRF cookie as a
    # response in case of a successful login
    @method_decorator(ensure_csrf_cookie)
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

        # generating auth token and refresh token
        auth_token = generate_auth_token(user=user)
        refresh_token, expiry = generate_refresh_token(user=user)

        # storing the cookie in the response
        response.set_cookie(key='refreshToken',
                            value=refresh_token,
                            expires=expiry,
                            httponly=True)
        response.data = {'auth_token': auth_token, 'user': serializer_user}
        return response


class UserView(views.APIView):
    """
    The default permission_class is IsAuthenticated, so a user needs
    to be authenticated in order to access this endpoint.
    """
    token_param_config = openapi.Parameter(
        'Authorization', in_=openapi.IN_HEADER, description='EXAMPLE: Token auth_token',
        type=openapi.TYPE_STRING, required=['Authorization'])

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request, *args, **kwargs):
        """
        Module for getting the current loggedIn user details
        """
        curr_user_email = request.user.email
        try:
            user_instance = USER.objects.get(email=curr_user_email)
        except USER.DoesNotExist:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

        user_data = UserSerializer(user_instance).data
        return Response(user_data)
