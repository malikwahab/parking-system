import os
from io import StringIO

from .base import *

from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))  # because the settings file is inside a folder
BASE_DIR = os.path.dirname(os.path.dirname(SETTINGS_DIR))

load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'), verbose=True)

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASS'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT'],
        'TEST': {
            'NAME': os.environ['TEST_DATABASE'],
        },
    }
}
