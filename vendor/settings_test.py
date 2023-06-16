# settings_test.py
import os
from .settings import *

# Use an in-memory SQLite database for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Set the app name
INSTALLED_APPS +=  [
    # 'store',
]

# Disable migrations during tests
MIGRATION_MODULES = {
    'store': None,
}

# Use a different media directory for tests
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
