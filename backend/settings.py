"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 2.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path helper
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                  '..', x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'fqBz9>xB:1\x0b:=e*S3&Df*rO#f=Ldu<x$0tXbnk]N9m,b7xgumQ')
#  \r+([xuhJM\\$S]78]h|#8EeOD'

# SECURITY WARNING: don't run with debug turned on in production!

if os.environ.get('ENV') == 'PRODUCTION':
    DEBUG = False
else:
    DEBUG = True

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party librairie
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    'storages',

    # local
    'api',  # endpoint app
    'users',  # app to manage users
]

AUTH_USER_MODEL = 'users.UserAccount'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 3rd
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 3rd
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': 5432
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = location('static')

STATICFILES_DIRS = [
    location("static/js/"),
    location("static/css/"),
    location("static/img/"),
]

# MEDIA SETTINGS
MEDIA_URL = '/media/'
MEDIA_ROOT = location('media/')

# Static files css for production

if os.environ.get('ENV') == 'PRODUCTION':
    """ Sometimes Django apps are deployed at a particular prefix
    (or “subdirectory”) on a domain e.g. http://example.com/my-app/ rather than
    just http://example.com. In this case you would normally use Django’s
    FORCE_SCRIPT_NAME setting to tell the application where it is located
    """
    # FORCE_SCRIPT_NAME = '/blog'
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATIC_ROOT = location('staticfiles')

    STATICFILES_DIRS = (location('static'), )
    # """ DROPBOX CONFIGURATION """
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

    DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/media'

    ADMIN_MEDIA_PREFIX = 'media'
    # "************ END DROPBOX CONFIGURATION ************"

    #  STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    # whitenoise.storage.CompressedManifestStaticFilesStorage
    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

# api configuration

# Disable browsable api in production
DEFAULT_RENDERER_CLASSES = ('rest_framework.renderers.JSONRenderer', )

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + (
        'rest_framework.renderers.BrowsableAPIRenderer', )

# REST framwork configuration
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS':
    ['django_filters.rest_framework.DjangoFilterBackend'],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        #  'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES':
    DEFAULT_RENDERER_CLASSES,
}

# Configuration for dj_rest_auth
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'

# SIMPLE_JWT configuration
SIMPLE_JWT = {
    'JWT_ALLOW_REFRESH': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': (
        'Bearer',
        'Token',
        'JWT',
    ),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

DJOSER = {
    "SERIALIZERS": {
        "user_create": "api.serializers.users.UserCreateSerializer",
        "user": "api.serializers.users.UserSerializer",
        "current_user": "api.serializers.users.UserSerializer",
    },
    "LOGIN_FIELD": "email",
    "PASSWORD_RESET_CONFIRM_URL": "auth/password/reset/{uid}/{token}",
}

# CORS HEADERS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://192.168.11.106:8080",
]

if os.environ.get('ENV') != 'PRODUCTION':
    CORS_ALLOWED_ORIGINS.append("http://localhost:3000")

# allows http verbs
from corsheaders.defaults import default_methods

CORS_ALLOW_METHODS = list(default_methods) + [
    #  "POKE",
]

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    #  "my-custom-header",
]

# Configuration for django resize
DJANGORESIZED_DEFAULT_SIZE = [400, 240]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg", 'PNG': ".png"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True
