# django
from django.db import models


class FormWizardTempFile(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)
