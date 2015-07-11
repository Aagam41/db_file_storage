# django
from django.core.urlresolvers import reverse
from django.db import models
# third party
from db_file_storage.model_utils import delete_file, delete_file_if_needed


class CDDisc(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class CDCover(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)


class CD(models.Model):
    name = models.CharField(max_length=100, unique=True)
    disc = models.ImageField(
        upload_to='model_filefields_example.CDDisc/bytes/filename/mimetype',
        blank=True,
        null=True
    )
    cover = models.ImageField(
        upload_to='model_filefields_example.CDCover/bytes/filename/mimetype',
        blank=True,
        null=True
    )

    def get_absolute_url(self):
        return reverse('model_files:cd.edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, 'disc')
        delete_file_if_needed(self, 'cover')
        super(CD, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super(CD, self).delete(*args, **kwargs)
        delete_file(self, 'disc')
        delete_file(self, 'cover')


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
