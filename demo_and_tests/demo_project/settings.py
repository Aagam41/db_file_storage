# -*- coding: utf-8 -*-

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Add db_file_storage directory to sys.path
DB_FILE_STORAGE_PATH = os.path.join(BASE_DIR, '..')
sys.path.append(DB_FILE_STORAGE_PATH)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'cj33louyit#jhcq%it)swv_(*_b$q%jv5%d8s-hjj#=l=swi^y'
ROOT_URLCONF = 'demo_project.urls'
WSGI_APPLICATION = 'demo_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('database.db')
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    #
    'db_file_storage',
    #
    'music',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware'
)

DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

TEST_FILES_DIR = os.path.join(BASE_DIR, 'files_for_testing')
