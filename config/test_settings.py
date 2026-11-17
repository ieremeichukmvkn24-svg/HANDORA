"""Test-only settings: isolated SQLite database for GitHub Actions."""
import os

# Explicit test-only key. Never used by deployed HANDORA.
os.environ.setdefault('SECRET_KEY', 'django-tests-only-do-not-use-in-production')

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
