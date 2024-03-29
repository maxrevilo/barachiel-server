import sys
from os import environ
from os.path import join
import dj_database_url
# from S3 import CallingFormat

# Local settings for the project.
try:
    from barachiel.settings.common import *
except ImportError as e:
    raise Exception('settings/common.py not available\n%s\n' % (str(e),))

#Don't use trailing slash!
BASE_URL = 'https://barachiel.herokuapp.com'

XS_SHARING_ALLOWED_ORIGINS = ''  # Overridden below if DEBUG=True

ADMINS = (
    ('Oliver Perez', 'oliver.a.perez.c@gmail.com'),
)

MIDDLEWARE_CLASSES += (
    'libs.middlewares.ssl_middleware.SSLMiddleware',
    'log_request_id.middleware.RequestIDMiddleware',
)

INSTALLED_APPS += (
    'djrill',
    'storages',
    'south',
)

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
# AWS_HEADERS = {
#     'Expires': 'Thu, 15 Apr 2010 20:00:00 GMT',
#     'Cache-Control': 'max-age=86400',
# }

# MEDIA_ROOT = join(PUBLIC_DIR, 'media')
MEDIA_URL = "http://s3.amazonaws.com/%s/" % AWS_STORAGE_BUCKET_NAME
STATIC_ROOT = join(PUBLIC_DIR, 'static/')
STATIC_URL = '/static/'

DEBUG = environ.get('DJANGO_DEBUG', 'False') == 'True'
LOGTAILER_HISTORY_LINES = 1000
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CONN_MAX_AGE = 60

# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': dj_database_url.config()
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Make this unique, and don't share it with anybody.
SECRET_KEY = environ['DJANGO_SECRET_KEY']

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = "587"
# EMAIL_HOST_USER = 'contact@waving.com'
# EMAIL_HOST_PASSWORD = '<your email password>'
# EMAIL_USE_TLS = True


# Logging for Heroku
LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
LOG_REQUESTS = True

LOGGING["filters"]['request_id'] = {
    '()': 'log_request_id.filters.RequestIDFilter'
}

LOGGING["formatters"]['standard'] = {
    'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
}

LOGGING['loggers']["django"] = {
    "handlers": ["console"],
}

LOGGING['loggers']["log_request_id.middleware"] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}

LOGGING['handlers']["console"] = {
    "level": "INFO",  # 'DEBUG',
    "class": "logging.StreamHandler",
    'stream': sys.stdout,
    'filters': ['request_id'],
    'formatter': 'standard',
}


if not DEBUG:
    MANDRILL_API_KEY = environ['MANDRILL_API_KEY']
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

if DEBUG:
    # Show emails in the console during development.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    XS_SHARING_ALLOWED_ORIGINS = '*'
