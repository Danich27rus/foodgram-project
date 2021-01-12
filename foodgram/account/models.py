from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    DJADMIN = 'djadmin'
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLES, default='user')
    # confirmation_code = models.CharField(max_length=200, default='FOOBAR')
