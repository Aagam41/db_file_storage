========================
django-db-file-storage
========================

Django DB File Storage is a custom
`file storage system <https://docs.djangoproject.com/en/dev/topics/files/#file-storage>`_
for Django. Use it to save your models' FileFields in your database instead of your file system.

How to use
========================

Installing
------------------------

If you still haven't done it, install django-db-file-storage in your environment by typing the following code on your shell::

    pip install django-db-file-storage

Settings
------------------------

On your project's settings, add ``'db_file_storage'`` to your
`INSTALLED_APPS list <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_.

Still on your project's settings, set `DEFAULT_FILE_STORAGE <https://docs.djangoproject.com/en/dev/ref/settings/#default-file-storage>`_ like this::
    
    DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'
    
URLs
------------------------

Add the following URL pattern to your project's main urlpatterns (/urls.py)::
    
    url(r'^files/', include('db_file_storage.urls')),
    
Models
------------------------

For each FileField you want to save, you will need a separated model to hold the file in the database. I will refer to this extra model as the **FileModel**. The FileModel must have at least these fields:

* a ``TextField()`` which will hold the encoded contents of the file
* a ``CharField(max_length=255)`` which will hold the file's name
* a ``CharField(max_length=50)`` which will hold the file's MIME type

For example (in a models.py file, inside an app called 'console')::

    from django.db import models
    
    class ConsolePicture(models.Model):
        bytes = models.TextField()
        filename = models.CharField(max_length=255)
        mimetype = models.CharField(max_length=50)
    
And the class which will have the FileField::
    
    class Console(models.Model):
        name = models.CharField(max_length=100)
        picture = models.ImageField(upload_to='console.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)

In this example, the FileField is actually an ImageField. It's ``upload_to`` argument must be a string in the following format:

1. the FileModel's app's name
2. a dot (.)
3. the FileModel's name
4. a forward slash (/)
5. the name of the FileModel's field which will hold the encoded contents of the files
6. a forward slash
7. the name of the FileModel's field which will hold the name of the files
8. a forward slash
9. the name of the FileModel's field which will hold the MIME type of the files

Let's check it again::
    
    #   1   2       3      4  5  6    7   8    9
    'console.ConsolePicture/bytes/filename/mimetype'

Don't forget to create the necessary tables in your database, if you haven't yet.

If you want stale files to be deleted when editing and deleting instances, override the ``save`` and ``delete`` methods of your model, calling ``db_file_storage.model_utils.delete_file_if_needed`` and ``db_file_storage.model_utils.delete_file`` inside them, respectively::

    from db_file_storage.model_utils import delete_file, delete_file_if_needed
    from django.db import models
    
    class Console(models.Model):
        name = models.CharField(max_length=100, unique=True)
        picture = models.ImageField(upload_to='console.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)
    
        def save(self, *args, **kwargs):
            delete_file_if_needed(self, 'picture')
            super(Console, self).save(*args, **kwargs)
    
        def delete(self, *args, **kwargs):
            super(Console, self).delete(*args, **kwargs)
            delete_file(self, 'picture')

Pay extra attention here to when the methods should be called. ``delete_file_if_needed`` should be called **before** the ``save`` method of the super class, and ``delete_file`` should be called **after** the ``delete`` method of the super class.

Form widget
------------------------

At this point, your project already must be saving files in the database when you use Django's ModelForms.

However, due to Django DB File Storage's internal logic, Django's default widget for file inputs won't show the proper filename when downloading uploaded files. The download itself works perfectly, it's just the widget that doesn't show the correct name in it's download link.

Django DB File Storage comes with a custom widget to solve this problem: DBClearableFileInput. You just need to use it when defining your form class::
    
    from console.models import Console
    from db_file_storage.form_widgets import DBClearableFileInput
    from django import forms
    
    class ConsoleForm(forms.ModelForm):
        class Meta:
            model = Console
            exclude = []
            widgets = {
                'picture': DBClearableFileInput
            }

Admin Form widget
~~~~~~~~~~~~~~~~~~~~~~~~

In order to solve the same problem in the `Django Admin <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_ interface, Django DB File Storage comes with another custom widget: DBAdminClearableFileInput. You just need to use it when defining your form class, and then `use such form when defining your ModelAdmin class <https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.form>`_ inside your ``admin.py`` file::
    
    from console.models import Console
    from db_file_storage.form_widgets import DBAdminClearableFileInput
    from django import forms
    from django.contrib import admin
    
    class ConsoleForm(forms.ModelForm):
        class Meta:
            model = Console
            exclude = []
            widgets = {
                'picture': DBAdminClearableFileInput
            }
    
    class ConsoleAdmin(admin.ModelAdmin):
        form = ConsoleForm
        
Downloading (and viewing) the files
---------------------------------------

Django DB File Storage comes with views that you can use to download the files or to just view them (for images, for example). They are accessed through the `named url patterns <https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns>`_ **db_file_storage.download_file** and **db_file_storage.get_file**.

Both views must be passed a GET parameter named ``name``, and the value of this parameter must be the value of the filefield of the instance. The template-snippet example below must make it clearer; ``console`` is an instance of the ``Console`` model defined above::

    <!-- The url used to VIEW the file: -->
    <img src="{% url 'db_file_storage.get_file' %}?name={{ console.picture }}" />

    <br/>

    <!-- The url used to DOWNLOAD the file: -->
    <a href='{% url "db_file_storage.download_file" %}?name={{ console.picture }}'>
        <i>Click here to download the picture</i>
    </a>

Demo
========================

In order to run the demo project, just

#. download the project and ``cd`` into it,
#. ``cd`` into the ``demo_and_tests`` directory,
#. `pip install <https://pypi.python.org/pypi/pip>`_ all the libraries specified in the `requirements file <https://github.com/victor-o-silva/db_file_storage/blob/master/demo_and_tests/requirements.txt>`_ in your environment (you might want to create and use a `virtual environment <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_),
#. run ``python manage syncdb`` and ``python manage runserver`` from your shell and
#. visit `http://localhost:8000 <http://localhost:8000>`_ in your browser.

Tests & Contributing
========================

In order to run the tests and contribute to db_file_storage, check the instructions in the `CONTRIBUTING file <https://github.com/victor-o-silva/db_file_storage/blob/master/CONTRIBUTING.rst>`_.