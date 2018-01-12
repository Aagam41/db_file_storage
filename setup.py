# -*- coding: utf-8 -*-

import os
from distutils.core import setup

readme_file = open('README.rst')

setup(
    name='django-db-file-storage',
    version='0.4.6',
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    packages=['db_file_storage'],
    package_data={
        'db_file_storage': ['templates/db_file_storage/widgets/*']
    },
    url='https://github.com/victor-o-silva/db_file_storage',
    download_url='https://github.com/victor-o-silva/db_file_storage'
                 '/tarball/0.4.6',
    description="Custom FILE_STORAGE for Django. Saves files "
                "in your database instead of your file system.",
    long_description=readme_file.read(),
    install_requires=[
        "Django",
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

readme_file.close()
