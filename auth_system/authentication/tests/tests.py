from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserTestCast(TestCase):

    def setUp(self):
        user_a = User.objects.create_user(
            username='test_username', email='test@email.com',
            password='test-password')
        self.user_a_pw = 'test-password'
        self.user_a = user_a

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)  # ==
        self.assertNotEqual(user_count, 0)  # !=

    def test_user_password(self):
        user_a = User.objects.get(email="test@email.com")
        self.assertTrue(
            user_a.check_password(self.user_a_pw)
        )

    def test_login_url(self):
        login_url = settings.LOGIN_URL
        data = {"email": "test@email.com", "password": "test-password"}
        response = self.client.post(login_url, data, follow=True)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
