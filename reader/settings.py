import getpass
import os


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'reader',
        'USER': getpass.getuser(),
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}

ALLOWED_HOSTS = ['*']
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
AUTH_USER_MODEL = 'users.User'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
DEFAULT_FROM_EMAIL = 'root@localhost'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

LOGIN_URL = '/login/'

SECRET_KEY = 'vx&62u*!d%t#6c8764r20e5#(tze0*$31z1^eur@&w0%yn6^8t'

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
    'pipeline',
    'reader.users',
    'reader',
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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

READER_TOKEN_EXPIRE = 2  # Expire login tokens after 2 hours.
READER_UPDATE_PROCESSES = 3  # Number of worker processes to use when updating feeds.

# Pipeline

PIPELINE = {
    'PIPELINE_ENABLED': False,
    'JS_COMPRESSOR': None,
    'CSS_COMPRESSOR': None,
    'DISABLE_WRAPPER': True,
    'JAVASCRIPT': {
        'reader': {
            'source_filenames': (
                'reader/js/spin.js',
                'reader/js/reader.js',
            ),
            'output_filename': 'reader.js',
        },
    },
    'STYLESHEETS': {
        'reader': {
            'source_filenames': (
                'reader/css/font-awesome.css',
                'reader/css/reader.css',
            ),
            'output_filename': 'reader.css',
        },
    },
}

local_settings_path = os.path.join(os.path.dirname(__file__), 'local_settings.py')
if os.path.exists(local_settings_path):
    with open(local_settings_path, 'r') as fp:
        exec(fp.read())
