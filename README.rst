========================
django-db-file-storage
========================

.. image:: https://travis-ci.org/victor-o-silva/db_file_storage.svg?branch=master
   :target: https://travis-ci.org/victor-o-silva/db_file_storage
   :alt: Build Status

.. image:: https://landscape.io/github/victor-o-silva/db_file_storage/master/landscape.svg?style=flat
   :target: https://landscape.io/github/victor-o-silva/db_file_storage/master
   :alt: Code Health

.. image:: https://coveralls.io/repos/victor-o-silva/db_file_storage/badge.svg?branch=master
   :target: https://coveralls.io/r/victor-o-silva/db_file_storage?branch=master
   :alt: Code Coverage

.. image:: http://readthedocs.org/projects/django-db-file-storage/badge/?version=master
   :target: http://django-db-file-storage.readthedocs.org/en/master/?badge=master
   :alt: Documentation Status

.. image:: https://badge.fury.io/py/django-db-file-storage.svg
   :target: https://badge.fury.io/py/django-db-file-storage

Django DB File Storage is a custom
`file storage system <https://docs.djangoproject.com/en/dev/topics/files/#file-storage>`_
for Django. Use it to save files in your database instead of your file system.

Supports Python versions ``2.7``, ``3.4`` & ``3.5``, and Django versions ``1.8`` & ``1.9``.

``Python 3.3``, ``Django 1.6`` and ``Django 1.7`` are not supported anymore. If you HAVE to stick with them, you can use Django DB File Storage 0.3.3 `(PyPI) <https://pypi.python.org/pypi/django-db-file-storage/0.3.3>`_ `(GitHub) <https://github.com/victor-o-silva/db_file_storage/releases/tag/0.3.3>`_.

Documentation
========================

The project docs can be found `here (RTD) <http://django-db-file-storage.readthedocs.org/en/master/>`_.

Demo
========================

In order to run the demo project, just

#. download the project and ``cd`` into it,
#. ``cd`` into the ``demo_and_tests`` directory,
#. `pip-install <https://pypi.python.org/pypi/pip>`_ all the libraries specified in the `requirements file <https://github.com/victor-o-silva/db_file_storage/blob/master/demo_and_tests/requirements.txt>`_ in your environment (you might want to create and use a `virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_),
#. run ``python manage.py migrate`` and ``python manage.py runserver`` from your shell and
#. visit `http://localhost:8000 <http://localhost:8000>`_ in your browser.

Tests & Contributing
========================

In order to run the tests and contribute to db_file_storage, check the instructions in the `CONTRIBUTING file <https://github.com/victor-o-silva/db_file_storage/blob/master/CONTRIBUTING.rst>`_.
