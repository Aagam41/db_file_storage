===============================
Contributing to db_file_storage
===============================

Issues reporting and pull requests are welcome!

For pull requests, please follow the topics below.

Python coding conventions
------------------------------

We try to comply with `pep-8 <https://www.python.org/dev/peps/pep-0008/>`_ wherever possible.
Code from pull requests should do the same.

Tests
------------------------------

The project with db_file_storage's automated tests is in the
`demo_and_tests <https://github.com/victor-o-silva/db_file_storage/tree/master/demo_and_tests>`_ directory.

Before creating a pull request, add/expand tests for your changes if needed and make sure that all tests are passing.

In order to test your branch of db_file_storage, you'll have to

#. ``cd`` into the ``demo_and_tests`` directory,
#. `pip install <https://pypi.python.org/pypi/pip>`_ all the libraries specified in the `requirements file <https://github.com/victor-o-silva/db_file_storage/blob/master/demo_and_tests/requirements.txt>`_ in your environment (you might want to create and use a `virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_),
#. run ``python manage.py test`` from your shell.
