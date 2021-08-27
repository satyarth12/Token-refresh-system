# from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
# Create your models here.


class CustomUser(AbstractUser):
    objects = CustomUserManager()
