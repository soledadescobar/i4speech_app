import os
import sys
import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(PROJECT_ROOT, 'src'))

SECRET_KEY = 'r4i^suffk0dushnc#h42%&ahxg1a8!y9j$f!pq@p)65o=myk@i'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'raven.contrib.django.raven_compat',
    'corsheaders',
    # 'django_celery_results',
    # 'django_celery_beat',
    'django_extensions',
    'rest_framework',
    'bootstrap3',
    'corecontrol',
    'dashboard',
    'search',
    'control',
    'rest',
    'twistreapy'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'src.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'managecenter',
        'USER': 'postgres',
        'PASSWORD': 'gorila38',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'rest': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'i4media_phase2',
        'USER': 'postgres',
        'PASSWORD': 'gorila38',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'twistreapy': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'i4media_phase2',
        'USER': 'postgres',
        'PASSWORD': 'gorila38',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASE_ROUTERS = ['twistreapy.routers.TwistreapyDatabaseRouter', ]

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://10.128.0.3:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

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

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # django.contrib.staticfiles.finders.DefaultStorageFinder',
)

BOOTSTRAP3 = {
    'javascript_in_head': True,
    'include_jquery': True,
}

LOGIN_REDIRECT_URL = 'index'

RAVEN_CONFIG = {
    'dsn': 'https://4b7210f68ae84d1eb0fd9af389f2e643:57c9720a50bd48fba55bff9f82301c03@sentry.io/204330',
}

SUIT_CONFIG = {
    'ADMIN_NAME': 'i4Media Suite',
    'MENU_ICONS': {
        'control': 'icon-list-alt',
        'corecontrol': 'icon-cog',
        'search': 'icon-search',
        'auth': 'icon-lock',
    },
}

# REDIS_HOST = '10.128.0.3'
# REDIS_PORT = 6379
# REDIS_DB = 0
# REDIS_PUSH = 'stream'
#
# CELERY_RESULT_BACKEND = 'django-cache'
# CELERY_BROKER_URL = 'redis://%s:%d/%d' % (REDIS_HOST, REDIS_PORT, REDIS_DB)
# CELERY_TASK_SERIALIZER = 'pickle'
# CELERY_RESULT_SERIALIZER = 'pickle'
# CELERY_ACCEPT_CONTENT = ['pickle']
# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
