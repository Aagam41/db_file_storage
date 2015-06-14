=========================
db_file_storage_tests
=========================

Demo and test suite for `db_file_storage <https://github.com/victor-o-silva/db_file_storage>`_ project.

Demo
=========================

To view the demo, just

#. download the project,
#. ``cd`` into its directory,
#. ``pip install`` all the libraries specified in the `requirements file <https://github.com/victor-o-silva/db_file_storage_tests/blob/master/requirements.txt>`_ in your environment,
#. run ``python manage syncdb`` and ``python manage runserver`` from your shell and
#. visit `http://localhost:8000 <http://localhost:8000>`_ in your browser.

Testing your db_file_storage fork
===================================

To test your fork of db_file_storage, you'll have to

#. download the project,
#. ``cd`` into its directory,
#. ``pip install`` **almost** all the libraries specified in the `requirements file <https://github.com/victor-o-silva/db_file_storage_tests/blob/master/requirements.txt>`_ in your environment (just don't install ``django-db-file-storage``),
#. copy the ``db_file_storage`` directory from your fork inside the ``db_file_storage_tests`` directory (on the same level as the directory of the ``music`` app),
#. run ``python manage test`` from your shell.

That will run the tests.

If needed, add more tests (or expand the ones already created) to test the changes you are making to your db_file_storage fork.

