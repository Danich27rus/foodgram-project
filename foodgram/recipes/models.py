from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    DJADMIN = "djadmin"
    ROLES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
        (DJADMIN, 'djadmin'),
    )
    bio = models.TextField(max_length=500, blank=True, null=True)
    role = models.CharField(max_length=30, choices=ROLES, default='user')
    confirmation_code = models.CharField(max_length=200, default='FOOBAR')


class Units(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ingredients(models.Model):

    name = models.CharField(max_length=200)
    qty = models.IntegerField()
    unit = models.ManyToManyField(
                            Units,
    )
    
    def __str__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='meals/%Y-%m-%d')
    description = models.TextField()
    duration = models.IntegerField()
    ingredients = models.ManyToManyField(Ingredients)
    # tags = 
    slug = models.SlugField()
