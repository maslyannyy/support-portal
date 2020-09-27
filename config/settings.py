import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG')
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'constance',
    'constance.backends.database',

    'report_portal',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'helpers.middleware.ErrorMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 5,
    },
    'reports': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('REPORT_DB_HOST'),
        'PORT': os.environ.get('REPORT_DB_PORT'),
        'USER': os.environ.get('REPORT_DB_USER'),
        'PASSWORD': os.environ.get('REPORT_DB_PASSWORD'),
        'NAME': os.environ.get('REPORT_DB_NAME'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 5,
    }
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_DATABASE_PREFIX = 'constance:report_portal:'

CONSTANCE_CONFIG = {
    'FEED_TG_CHAT_ID': (0, 'Чат для нотификации по фидам', int),
    'SPAM_TG_CHAT_ID': (0, 'Чат для отправки спама', int),
    'JIRA_TG_CHAT_ID': (0, 'Чат для нотификации jira', int),
    'SPAM_TG_LAST_MESSAGE_ID': (0, 'Последнее сообщение в спам чате', int),
    'JIRA_DOMAIN': ('', 'Домен jira', str),
    'JIRA_LOGIN': ('', 'Логин для jira', str),
    'JIRA_PASSWORD': ('', 'Пароль для jira', str),
    'JIRA_FILTER_ID': (0, 'Номер фильтра для jira', int),
    'JIRA_LAST_TASK_ID': (0, 'Номер последней заявки в jira', int),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': '[{asctime}] {levelname}: {module} - {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'error.log'),
            'formatter': 'base',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'propagate': True,
        },
        'report-portal': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'tasks': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/reports/'

LOGOUT_REDIRECT_URL = '/login/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_'),
]
