from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

User = get_user_model()


class UserTestCase(APITestCase):

    def setUp(self):
        user = User.objects.create_user(
            username='test_username', email='test@email.com',
            password='test-password')
        self.user_pw = 'test-password'
        self.user = user

        self.api_client = APIClient()

        self.login_url = settings.LOGIN_URL
        data = {"email": "test@email.com", "password": "test-password"}
        self.login_response = self.api_client.post(
            self.login_url, data, follow=True, format='json')

        self.auth_token = self.login_response.json()['auth_token']

    def test_user_details(self):
        # addding the auth header to the client
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.auth_token)

        user_detail_url = '/auth/user-details/'
        response = self.api_client.get(
            user_detail_url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_expired_details(self):
        """
        Unittest for checking if the auth token is expire or not
        """
        expired_auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJleHAiOjE2MzAxMTczMzgsImlhdCI6MTYzMDExNzAzOH0.3_XotEEvvY-GdsHsZzA0mD4sVJIzmWRv4PsD5PZTvJc"

        # addding the auth header to the client
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Token ' + expired_auth_token)

        user_detail_url = '/auth/user-details/'
        response = self.api_client.get(
            user_detail_url
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regenerate_auth_token(self):
        new_auth_url = '/auth/token/new-auth-token/'
        response = self.api_client.get(
            new_auth_url
        )
        self.assertTrue('auth_token' in response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
