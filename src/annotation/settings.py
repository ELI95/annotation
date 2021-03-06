"""
Django settings for annotation project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import pymysql
import djcelery

from annotation.restconf.main import *


# django-celery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERY_IMPORTS = (
    'tasks.tasks',
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jm#x%htdd#dmho_8%pxlv*+hkrkg--0&xx-r(3w(+!_+$yp1(1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'djcelery',
    'accounts',
    'projects',
    'tasks',
    'targets',
    'tags',
    'quizzes',
    'grades',
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

ROOT_URLCONF = 'annotation.urls'

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

WSGI_APPLICATION = 'annotation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'annotation',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'


# Media files

MEDIA_URL = 'http://10.1.62.101/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

# Quiz files

QUIZ_URL = 'http://10.1.62.101/media/quiz/'

QUIZ_ROOT = os.path.join(MEDIA_ROOT, 'quiz')

# Label files

LABEL_URL = 'http://10.1.62.101/media/quiz/label/'

LABEL_ROOT = os.path.join(QUIZ_ROOT, 'label')

# Result files

RESULT_URL = 'http://10.1.62.101/result/'

RESULT_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'result')


# Custom user model
AUTH_USER_MODEL = 'accounts.User'
