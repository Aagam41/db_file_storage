# django
from django.db import models
# third party
from db_file_storage.model_utils import delete_file, delete_file_if_needed
from db_file_storage.compat import reverse


class BookIndex(models.Model):
    book_index_pk = models.AutoField(primary_key=True)
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class BookPages(models.Model):
    book_pages_pk = models.AutoField(primary_key=True)
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class BookCover(models.Model):
    book_cover_pk = models.AutoField(primary_key=True)
    bytes = models.BinaryField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class Book(models.Model):
    book_pk = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    index = models.FileField(
        upload_to='model_filefields_example.BookIndex/bytes/filename/mimetype',
        blank=True, null=True
    )
    pages = models.FileField(
        upload_to='model_filefields_example.BookPages/bytes/filename/mimetype',
        blank=True, null=True
    )
    cover = models.ImageField(
        upload_to='model_filefields_example.BookCover/bytes/filename/mimetype',
        blank=True, null=True
    )

    def get_absolute_url(self):
        return reverse('model_files:book.edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'index')
        delete_file_if_needed(self, 'pages')
        super(Book, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(Book, self).delete(*args, **kwargs)
        delete_file(self, 'index')
        delete_file(self, 'pages')

    def __str__(self):
        return self.name


class SoundDeviceInstructionManual(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class SoundDevice(models.Model):
    name = models.CharField(max_length=100)
    instruction_manual = models.FileField(
        upload_to='model_filefields_example.SoundDeviceInstructionManual'
                  '/bytes/filename/mimetype',
        blank=True,
        null=True
    )
