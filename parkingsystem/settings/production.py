from .base import *
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.config()
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['.herokuapp.com']
