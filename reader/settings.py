import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reader',
        'USER': 'reader',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
AUTH_USER_MODEL = 'reader.User'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_FROM_EMAIL = 'root@localhost'

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
LOGIN_URL = '/login/'

STATICFILES_DIRS = (
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = 'vx&62u*!d%t#6c8764r20e5#(tze0*$31z1^eur@&w0%yn6^8t'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'reader.utils.reader_context',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'reader.urls'

WSGI_APPLICATION = 'reader.wsgi.application'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'haystack',
    'reader',
    'compressor',
    'tastypie',
    'south',
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = (
    'reader.backends.EmailTokenBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'reader',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

SESSION_COOKIE_NAME = 'reader-session'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4 # 4 weeks in seconds

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

COMPRESS_ENABLED = True

READER_TOKEN_EXPIRE = 24 # Expire login tokens after 2 hours.
READER_UPDATE_PROCESSES = 3 # Number of worker processes to use when updating feeds.

try:
    from local_settings import *
except:
    pass
