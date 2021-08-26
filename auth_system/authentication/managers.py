from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError(_('User must have a username'))

        if not password:
            raise ValueError(_('User must have a password'))

        if not email:
            raise ValueError(_('User must have an email'))

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
