# -*- coding: utf-8 -*-

from distutils.core import setup

readme_file = open('README.rst')

setup(
    name='django-db-file-storage',
    version='0.4.2',
    author='Victor Oliveira da Silva',
    author_email='victor_o_silva@hotmail.com',
    packages=['db_file_storage'],
    url='https://github.com/victor-o-silva/db_file_storage',
    download_url='https://github.com/victor-o-silva/db_file_storage'
                 '/tarball/0.4.2',
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
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

readme_file.close()
