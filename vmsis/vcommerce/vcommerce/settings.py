"""
Django settings for vcommerce project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from vlib import menu_apps

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOTDIR  = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fhtdji%*)+2d5-0xwnyp=mfxe=9*-_^9t8+dji%4eqv@bnx-pd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS_BASE = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vlib',
    'vlib.control',
)

INSTALLED_APPS = INSTALLED_APPS_BASE + menu_apps.MenuApps.GetAppsOnMenu()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'vcommerce.urls'

WSGI_APPLICATION = 'vcommerce.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases



DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'vcommerce',
#        'HOST': 'postgres48797-vcommerce.jelasticlw.com.br\\vcommerce',
#        'USER': 'webadmin',
#        'PASSWORD': 'OhuIlj6NDR',
#        'PORT': '',
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_URL = '/vlib/skin/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "vlib/skin")
ADMIN_MEDIA_PREFIX = '/media/'

STATIC_URL = '/vlib/skin/static/'
#STATIC_URL = '/static/' for deploy
STATIC_ROOT = os.path.join(BASE_DIR, '../../static')


TEMPLATE_DIRS = (os.path.join(BASE_DIR,'vlib/skin/template'),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "vlib/skin"),
)

FIXTURE_DIRS = (
    os.path.join(BASE_DIR,'cadastro/fix/'),
)