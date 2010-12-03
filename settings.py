# Django settings for ecoledzu project.

import socket,os
PROJECT_NAME = os.path.basename(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = '%s/../..' % PROJECT_PATH
MEDIA_ROOT = PROJECT_PATH + '/media/'
MEDIA_URL = '/media/'
MEDIA_PREFIX = '/media/'
CSS_ROOT = PROJECT_PATH + '/css/'
JS_ROOT = PROJECT_PATH + '/js/'
JS_LIB_ROOT = PROJECT_PATH + '/lib/'
IMAGES_ROOT = PROJECT_PATH + '/img/'
  
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

EMAIL_HOST = "smtp.gmail.com"
#EMAIL_PORT = 587
EMAIL_HOST_USER = 'autrusseau.damien@gmail.com'
EMAIL_HOST_PASSWORD = 'WsMCGFMh'
EMAIL_USE_TLS = True

DATABASES = {
    'default': {
        'ENGINE': 'mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pokermagique',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}    


TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'fr-fr'
SITE_ID = 1
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'c%!=aw62vxrk_%sdhi9eu=_krshj@ho(=evuo++da=xyufdb*&'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
ROOT_URLCONF = '%s.urls' % PROJECT_NAME
TEMPLATE_DIRS = (
    os.path.dirname(os.path.abspath(__file__))
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',    
    #'south',
    'room',
    'player',
)

# DEVELOPMENT settings
if socket.gethostname().find( "gne" ) != -1:
    DATABASE_PASSWORD = ''
    #SOUTH_AUTO_FREEZE_APP = True
