# Global settings for the project.
import sys
import string
from os.path import join, abspath, dirname

PROJECT_DIR = abspath(join(dirname(__file__), '../../'))
PUBLIC_DIR = join(PROJECT_DIR, 'public')

# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'UTC'

# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
SITE_NAME = "Waving"

USE_I18N = False
USE_L10N = False
USE_TZ = False

APPEND_SLASH = True

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
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    # 3rd Party middlewares:
    'libs.middlewares.crossdomainxhr.XsSharingMiddleware'
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
DISPOSABLE_EMAIL_DOMAINS = join(PROJECT_DIR, "static/disposable_email_domains.txt")

SESSION_COOKIE_AGE = 2419200
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
    'apps.likes',
    'apps.multimedia',
    'apps.debug_gps',
    # 3rd Party Apps:
    'logtailer',
    'sorl.thumbnail',
    'disposable_email_checker',
    # 'django_inlinecss',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
