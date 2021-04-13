import os
import toml

from typing import List, Any, Union, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

toml_config = toml.load(os.path.join(BASE_DIR, 'config.toml'))

SECRET_KEY = toml_config['main']['secret_key']
DEBUG = (toml_config['main'].get("debug", True))

ALLOWED_HOSTS = toml_config['main']['allowed_hosts']

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps
    'apps.timetable.apps.TimetableConfig',
    'apps.minimum.apps.MinimumConfig',
    'apps.diary.apps.DiaryConfig',
    'apps.news.apps.NewsConfig',
    'apps.klasses.apps.KlassesConfig',
    'apps.homework.apps.HomeworkConfig',
    'apps.admin_panel',
    'apps.accounts',
    'apps.api',
    'apps.core',
    'apps.notes',
    # Third party
    'rest_framework',  # Working with API
    'rest_framework.authtoken',  # Token authentication for REST API
    'django_cleanup',  # Deleting unused files in storage
    'debug_toolbar',  # Displaying debug info
    'django_extensions',  # Advances manage.py functions
    'django_filters',  # Filtering support for API
    'widget_tweaks',  # Useful functions for working with forms in templates
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

ROOT_URLCONF = 'school_diary.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'core.Users'

WSGI_APPLICATION = 'school_diary.wsgi.application'

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': toml_config['database']['postgres']['name'],
            'USER': toml_config['database']['postgres']['user'],
            'PASSWORD': toml_config['database']['postgres']['password'],
            'HOST': toml_config['database']['postgres']['host'],
            'PORT': toml_config['database']['postgres'].get("port", ""),
            'ATOMIC_REQUESTS': True,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': toml_config['database']['sqlite'].get("name", "db.sqlite3"),
            'ATOMIC_REQUESTS': True,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
else:
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ACCOUNT_AUTHENTICATION_METHOD = 'email'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = toml_config['email']['host']
EMAIL_PORT = toml_config['email']['port']
EMAIL_USE_TLS = toml_config['email']['use_tls']
EMAIL_USE_SSL = toml_config['email']['use_ssl']
EMAIL_HOST_USER = toml_config['email']['address']
EMAIL_HOST_PASSWORD = toml_config['email']['password']
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


ADMINS = toml_config['other']['admins']


if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/home/alan/diary/logs/warning.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
}

GRADES: List[Union[Tuple[int, int], Any]] = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    (11, 11)
]

LETTERS: List[Tuple[str, str]] = [
    ("А", "А"),
    ("Б", "Б"),
    ("В", "В"),
    ("Г", "Г"),
    ("Д", "Д"),
    ("Е", "Е"),
    ("Ж", "Ж"),
    ("З", "З"),
    ("И", "И"),
    ("К", "К")
]

ACCOUNT_TYPES = [
    (0, "Root"),
    (1, "Администратор"),
    (2, "Учитель"),
    (3, "Ученик"),
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
