import dj_database_url

import binascii
import os


def get_secret(name, default='', cast=str):
    value = os.getenv(name.upper())
    if value is not None:
        return cast(value)
    try:
        with open('/etc/secrets/%s' % name.lower(), 'r') as f:
            return cast(f.read().strip())
    except FileNotFoundError:
        return default


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SECRET_KEY = get_secret('SECRET_KEY', binascii.hexlify(os.urandom(32)).decode('ascii'))

DEBUG = get_secret('DEBUG', 'true').lower() in ('true', '1')
ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS', '*').split(',')

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': dj_database_url.config(default='postgres:///reader', conn_max_age=600),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True

TIME_ZONE = get_secret('TIME_ZONE', 'America/New_York')
LANGUAGE_CODE = get_secret('LANGUAGE_CODE', 'en-us')

USE_I18N = True
USE_L10N = True
USE_TZ = True

SITE_ID = 1

DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL', 'root@localhost')
EMAIL_BACKEND = get_secret('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend')

STATIC_ROOT = get_secret('STATIC_ROOT', os.path.join(BASE_DIR, 'static'))
STATIC_URL = get_secret('STATIC_URL', '/static/')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'reader.utils.reader_context',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reader.urls'
WSGI_APPLICATION = 'reader.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'reader.users',
    'reader',
)

AUTHENTICATION_BACKENDS = (
    'reader.backends.EmailTokenBackend',
)

SESSION_COOKIE_NAME = 'reader-session'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4  # 4 weeks in seconds

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
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'reader.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'reader': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }
}

READER_TOKEN_EXPIRE = get_secret('READER_TOKEN_EXPIRE', 2, cast=int)  # Expire login tokens after 2 hours.
READER_UPDATE_PROCESSES = 3  # Number of worker processes to use when updating feeds.
