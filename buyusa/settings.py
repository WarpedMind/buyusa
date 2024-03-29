"""
Django settings for buyusa project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE_URL='https://www.buyusa.support'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$z-h&j3-_@uiz1++g1m3$f6znq+#f7lc!k+pej#5@9$nz7h=o_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'stormy-beach-97292.herokuapp.com', 'localhost', 'buyusa.support', 'www.buyusa.support']


# Application definition

INSTALLED_APPS = [
    'buyusaapp',    
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',    
    'social_django',
    'ckeditor',
    # 'ckeditor_uploader',
    'social.apps.django_app.default',
    'crispy_forms',
    # 'django_truncate',
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

ROOT_URLCONF = 'buyusa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'buyusa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# To serve static files on Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

CKEDITOR_BASEPATH = STATIC_URL + "ckeditor/ckeditor"
CKEDITOR_UPLOAD_PATH = "uploads/"

AUTHENTICATION_BACKENDS = {
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend'
}

# Registration
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL = '/welcome'
LOGIN_URL = '/accounts/login'

SOCIAL_AUTH_FACEBOOK_KEY = '136569393640886'
SOCIAL_AUTH_FACEBOOK_SECRET = 'dc2c5ae890d906791b88108430e43ba8'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'buyusaapp.social_auth_pipeline.save_avatar',  # <--- set the path to the function
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)
# Replace database setting to use postgresql on Heroku
import dj_database_url
db_from_env = dj_database_url.config()
#DATABASES['default'].update(db_from_env)

# Setup upload directory for Gig model
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Email settings
#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
DEFAULT_FROM_EMAIL = 'support@buyusa.support'
EMAIL_HOST = 'mail.blank.com'
EMAIL_HOST_USER = 'aplpe'
EMAIL_HOST_PASSWORD = 'applepie76'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'D:\\Projects\\GitHub\\buyusa_web\\test_emails' # change this to a proper location

CRISPY_FAIL_SILENTLY = not DEBUG
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
SEARCH_RESULTS_PER_PAGE = 24

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': { 'verbose': { 'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s' }, },
    'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'D:\\Projects\\GitHub\\buyusa_web\\buyusa.log',
                'formatter': 'verbose',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['file', 'console'],            
            'propagate': True,
        },
        'buyusa': {
            'level': 'INFO',
            'handlers': ['file', 'console'],
        },
    },
}
