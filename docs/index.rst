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
`INSTALLED_APPS tuple <https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps>`_.

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
    
    class ConsolePicture(models.Model):
        bytes = models.TextField()
        filename = models.CharField(max_length=255)
        mimetype = models.CharField(max_length=50)
    
And the class which will have the FileField::
    
    class Console(models.Model):
        name = models.CharField(max_length=100)
        picture = models.ImageField(upload_to='console.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)

In this example, the FileField is actually an ImageField. It's *upload_to* argument must be a string in the following format:

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

Form widget
------------------------

At this point, your project already must be saving files in the database when you use Django's ModelForms.

However, due to Django DB File Storage's internal logic, Django's default widget for file inputs won't show the proper filename when downloading uploaded files. The download itself works perfectly, it's just the widget that doesn't show the correct name in it's download link.

Django DB File Storage comes with a custom widget to solve this problem: DBClearableFileInput. You just need to use it when defining your form class::
    
    from console.models import Console
    from db_file_storage.form_widgets import DBClearableFileInput
    from django import forms
    
    class FormConsole(forms.ModelForm):
        class Meta:
            model = Console
            widgets = {
                'picture': DBClearableFileInput
            }
    
Code & Demo
========================

* Package Code: https://github.com/victor-o-silva/db_file_storage
* Demo Project: https://github.com/victor-o-silva/db_file_storage_demo



