"""Temporary local demo configuration for mobile screenshot workflow."""
from .test_settings import *  # noqa: F403,F401

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'demo_mobile.sqlite3',
    },
}

# Serve static files through Django's development server for screenshot capture only.
DEBUG = True
