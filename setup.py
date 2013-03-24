# -*- coding: utf-8 -*-

from distutils.core import setup


setup(
    name = 'django-db-file-storage',
    version = '0.1.0',
    author = 'Victor Oliveira da Silva',
    author_email = 'victor_o_silva@hotmail.com',
    packages = ['db_file_storage', 'db_file_storage.test'],
    scripts = [],
    url = 'http://pypi.python.org/pypi/DjangoDBFileStorage/',
    license = 'LICENSE.txt',
    description = "Custom FILE_STORAGE for Django. Saves model's filefields in your database instead of your file system.",
    long_description = open('README.txt').read(),
    install_requires=[
        "Django",
    ],
)
