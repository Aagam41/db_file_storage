# -*- coding: utf-8 -*-

# python imports
import base64
import sys

# django imports
from django import VERSION as DJ_VERSION
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse

if sys.version_info.major == 2:  # python2
    from urllib import urlencode
else:  # python3
    from urllib.parse import urlencode

# As of Django 1.7, the utilities in django.db.models.loading are
# deprecated (to be removed in 1.9) in favor of the the new
# application loading system. Check here:
# https://github.com/django/django/blob/1.7/django/db/models/loading.py
if DJ_VERSION[0] <= 1 and DJ_VERSION[1] <= 6:
    from django.db.models.loading import get_model
else:
    from django.apps import apps
    get_model = apps.get_model


def _get_model_class(model_class_path):
    app_label, model_name = model_class_path.rsplit('.', 1)
    return get_model(app_label, model_name)


def _get_encoded_bytes_from_file(_file):
    _file.seek(0)
    file_content = _file.read()
    return base64.b64encode(file_content)


def _get_file_from_encoded_bytes(encoded_bytes):
    file_buffer = base64.b64decode(encoded_bytes)
    return ContentFile(file_buffer)


def _get_unique_filename(model_class, filename_field, filename):
    final_name = filename

    if ('.' in filename.rsplit('/', 1)[-1]):
        stem, extension = final_name.rsplit('.', 1)
    else:
        stem, extension = (final_name, '')

    append_to_name = 1
    while model_class.objects.filter(**{filename_field: final_name}).exists():
        final_name = '%s_(%s)%s' % (
            stem,
            append_to_name,
            ('.%s' % extension) if extension else ''
        )
        append_to_name += 1
    return final_name


class DatabaseFileStorage(Storage):
    def _open(self, name, mode='rb'):
        assert mode[0] in 'rwab'
        (model_class_path, content_field, filename_field,
            mimetype_field, filename) = name.split('/')
        model_class = _get_model_class(model_class_path)
        model_instance = model_class.objects.only(
            content_field, mimetype_field
        ).get(**{filename_field: name})
        encoded_bytes = getattr(model_instance, content_field)
        _file = _get_file_from_encoded_bytes(encoded_bytes)
        _file.filename = filename
        _file.mimetype = getattr(model_instance, mimetype_field)
        return _file

    def _save(self, name, content):
        parts = name.split('/')
        model_class_path = parts[0]
        content_field = parts[1]
        filename_field = parts[2]
        mimetype_field = parts[3]
        model_class = _get_model_class(model_class_path)
        new_filename = _get_unique_filename(model_class, filename_field, name)
        encoded_bytes = _get_encoded_bytes_from_file(content)
        mimetype = getattr(content.file, 'content_type', 'text/plain')
        model_class.objects.create(**{
            content_field: encoded_bytes,
            filename_field: new_filename,
            mimetype_field: mimetype,
        })
        return new_filename

    def delete(self, name):
        parts = name.split('/')
        model_class_path = parts[0]
        filename_field = parts[2]
        model_class = _get_model_class(model_class_path)
        model_class.objects.filter(**{filename_field: name}).delete()

    def exists(self, name):
        parts = name.split('/')
        model_class_path = parts[0]
        filename_field = parts[2]
        filename = parts[4]
        model_class = _get_model_class(model_class_path)
        return model_class.objects.filter(
            **{filename_field: filename}
        ).exists()

    def url(self, name):
        _url = reverse('db_file_storage.download_file')
        return _url + '?' + urlencode({'name': name})
