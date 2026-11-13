"""Test-only settings: isolated SQLite database for GitHub Actions."""
from .settings import *  # noqa: F403,F401

SECRET_KEY = 'only-for-unit-tests-not-for-deployment'
DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
