# -*- coding: utf-8 -*-

from distutils.core import setup

readme_file = open('README.rst')

VERSION = '0.5.4'

setup(
    name='django-db-file-storage',
    version=VERSION,
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    packages=['db_file_storage'],
    package_data={
        'db_file_storage': ['templates/db_file_storage/widgets/*']
    },
    url='https://github.com/victor-o-silva/db_file_storage',
    download_url='https://github.com/victor-o-silva/db_file_storage'
                 '/tarball/{}'.format(VERSION),
    description="Custom FILE_STORAGE for Django. Saves files "
                "in your database instead of your file system.",
    long_description=readme_file.read(),
    install_requires=[
        'Django',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

readme_file.close()
