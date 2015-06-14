# -*- coding: utf-8 -*-

from distutils.core import setup

readme_file = open('README.rst')

setup(
    name='django-db-file-storage',
    version='0.2.12',
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    packages=['db_file_storage'],
    url='https://github.com/victor-o-silva/db_file_storage',
    download_url='https://github.com/victor-o-silva/db_file_storage'
                 '/tarball/0.2.12',
    license='GNU GPL v3',
    description="Custom FILE_STORAGE for Django. Saves model's filefields "
                "in your database instead of your file system.",
    long_description=readme_file.read(),
    install_requires=[
        "Django",
    ],
)

readme_file.close()
