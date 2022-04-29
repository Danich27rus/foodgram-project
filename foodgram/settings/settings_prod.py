import environ
import os

from pathlib import Path
from .settings import *

env = environ.Env()
environ.Env.read_env()

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS += [os.environ.get('DOMAIN_NAME')]

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MAILER_EMAIL_BACKEND = EMAIL_BACKEND

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')

EMAIL_HOST = os.environ.get('EMAIL_HOST')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

EMAIL_PORT = os.environ.get('EMAIL_PORT')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
