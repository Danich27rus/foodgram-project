import environ
import os

from pathlib import Path
from .settings import *

env = environ.Env()
environ.Env.read_env(os.path.dirname(os.path.realpath(__file__)) + "/.dev.env")

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS += ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
