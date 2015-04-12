# Global settings for the project.
import sys
import string
from os import environ
from os.path import join, abspath, dirname
from datetime import timedelta

PROJECT_DIR = abspath(join(dirname(__file__), '../../'))
PUBLIC_DIR = join(PROJECT_DIR, 'public')

TIME_TO_GHOSTING = timedelta(minutes=int(environ.get('WAVING_TIME_TO_GHOSTING', 120)))
RADAR_RAIUS = int(environ.get('WAVING_RADAR_RAIUS', 1000))
IGNORE_DISTANCE = environ.get('WAVING_IGNORE_DISTANCE', 'False') == 'True'

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_NAME = "Waving"

USE_I18N = False
USE_L10N = False
USE_TZ = False

# APPEND_SLASH = True

THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'

STATICFILES_DIRS = (
    string.replace(join(PROJECT_DIR, 'static/'), '\\', '/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    join(PROJECT_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    # Django Processors:
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    # 3rd Party Processors:
)

MIDDLEWARE_CLASSES = (
    # Django middlewares:
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    # 3rd Party middlewares:
    'libs.middlewares.crossdomainxhr.XsSharingMiddleware',
    'libs.middlewares.error_logging.ErrorLoggingMiddleware',
    'libs.middlewares.extend_user_session.ExtendUserSession',
)

ROOT_URLCONF = 'barachiel.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^.*$'
CORS_ALLOW_CREDENTIALS = False  # Cookies not alloew over CORS

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'barachiel.wsgi.application'

# Specify authentication model, so django-allauth knows which one to use:
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'apps.auth.backends.AuthBackend',
)

# $ wget https://raw.github.com/aaronbassett/DisposableEmailChecker/master/disposable_email_domains.txt
DISPOSABLE_EMAIL_DOMAINS = join(PROJECT_DIR, "libs/disposable_email_domains.txt")
EMAIL_SUBJECT_PREFIX = '[Waving] '
ACCOUNT_GRACE_TIME = 14
DEFAULT_FROM_EMAIL = 'contact@example.com'

SESSION_COOKIE_AGE = 5259487
#CSRF_FAILURE_VIEW = 'apps.auth.views.csrf_failure'

FIXTURE_DIRS = (
    join(PROJECT_DIR, 'fixtures'),
)

# Libraries
sys.path.insert(0, join(PROJECT_DIR, "libs/python-push/"))
sys.path.insert(0, join(PROJECT_DIR, "libs/asynchttp/"))
sys.path.insert(0, join(PROJECT_DIR, "libs/django-logtailer/"))

INSTALLED_APPS = (
    # Django Apps:
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # Barachiel Apps:
    'apps.auth',
    'apps.push',
    'apps.users',
    'apps.referrals',
    'apps.likes',
    'apps.multimedia',
    'apps.debug_gps',
    # 3rd Party Apps:
    'logtailer',
    'sorl.thumbnail',
    'disposable_email_checker',
    'django_rq',
    # 'django_inlinecss',
)

RQ_QUEUES = {
    'default': {
        'URL': environ.get('REDISTOGO_URL', 'redis://localhost:6379'),
        'DB': 0,
        'DEFAULT_TIMEOUT': 500,
    }
}
# WARN: DJANGO_RQ with "RQ_SHOW_ADMIN_LINK = True" might override the admin template
RQ_SHOW_ADMIN_LINK = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        "rq_console": {
            "level": "DEBUG",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        "rq.worker": {
            "handlers": ["rq_console"],
            "level": "DEBUG"
        },
    }
}
