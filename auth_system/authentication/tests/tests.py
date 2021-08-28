from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class UserTestCase(APITestCase):

    def setUp(self):
        user_a = User.objects.create_user(
            username='test_username', email='test@email.com',
            password='test-password')
        self.user_a_pw = 'test-password'
        self.user_a = user_a

        self.login_url = settings.LOGIN_URL
        self.register_url = '/auth/register/'

        self.api_client = APIClient()

    def test_user_registration(self):
        """
        Unittest for successfull user registration
        with status code 200
        """
        data = {
            'username': 'newtestuser',
            'email': 'newuser@xyz.com',
            'password': 'test-password'
        }
        response = self.api_client.post(self.register_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(
            response.json(), 'SignUp successfull. Please login to continue')
        self.assertEqual(status_code, 200)

    def test_error_user_registration(self):
        """
        Unittest for unsuccessfull user registration
        with status code 409
        """
        data = {
            'username': 'test_username',
            'email': 'test@email.com',
            'password': 'test-password'
        }
        response = self.api_client.post(self.register_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 409)

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)  # ==
        self.assertNotEqual(user_count, 0)  # !=

    def test_success_login_url(self):
        """
        Unittest for sucessull login with status code 200
        """
        data = {"email": "test@email.com", "password": "test-password"}
        response = self.api_client.post(self.login_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(list(response.client.cookies.items())
                         [0][0], 'refreshToken')
        self.assertTrue('auth_token' in response.json())
        self.assertEqual(status_code, 200)

    def test_error_login_url(self):
        """
        Unittest for unsucessull login with status code 403,
        but with different details
        """
        invalid_email_data = {
            "email": "invalid@gmail.com", "password": "test-password"}
        response = self.api_client.post(
            self.login_url, invalid_email_data, follow=True)
        status_code = response.status_code
        self.assertEqual(response.json()['detail'], 'User not found')
        self.assertEqual(status_code, 403)

        invalid_password_data = {
            "email": "test@email.com", "password": "invalid-password"
        }
        response = self.api_client.post(
            self.login_url, invalid_password_data, follow=True)
        status_code = response.status_code
        self.assertEqual(response.json()['detail'], 'Incorrect password')
        self.assertEqual(status_code, 403)
