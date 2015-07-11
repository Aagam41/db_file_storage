# python
import base64
import sys
# django
from django import VERSION as DJ_VERSION
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
from django.utils.crypto import get_random_string

if sys.version_info.major == 2:  # python2
    from urllib import urlencode
else:  # python3
    from urllib.parse import urlencode


class DatabaseFileStorage(Storage):
    """ File storage system that saves models' FileFields in the database.

        Intended for use with Models' FileFields.
        Uses a specific model for each FileField of each Model.
    """
    def __init__(self, *args, **kwargs):
        super(DatabaseFileStorage, self).__init__(*args, **kwargs)
        # As of Django 1.7, the utilities in django.db.models.loading are
        # deprecated (to be removed in 1.9) in favor of the the new
        # application loading system. Check here:
        # https://github.com/django/django/blob/1.7/django/db/models/loading.py
        if DJ_VERSION[0] == 1 and DJ_VERSION[1] < 7:
            from django.db.models.loading import get_model
        else:
            from django.apps import apps
            get_model = apps.get_model
        self._get_model = get_model

    def _get_model_cls(self, model_class_path):
        app_label, model_name = model_class_path.rsplit('.', 1)
        return self._get_model(app_label, model_name)

    def _get_encoded_bytes_from_file(self, _file):
        _file.seek(0)
        file_content = _file.read()
        return base64.b64encode(file_content)

    def _get_file_from_encoded_bytes(self, encoded_bytes):
        file_buffer = base64.b64decode(encoded_bytes)
        return ContentFile(file_buffer)

    def _get_unique_filename(self, model_cls, filename_field, filename):
        final_name = filename

        if ('.' in filename.rsplit('/', 1)[-1]):
            stem, extension = final_name.rsplit('.', 1)
        else:
            stem, extension = (final_name, '')

        random_str = get_random_string(7)
        while model_cls.objects.filter(
            **{filename_field: final_name}
        ).exists():
            final_name = '%s_(%s)%s' % (
                stem, random_str,
                ('.%s' % extension) if extension else ''
            )
            random_str = get_random_string(7)
        return final_name

    def _get_storage_attributes(self, name):
        (model_class_path, content_field, filename_field,
            mimetype_field, filename) = name.split('/')
        return {
            'model_class_path': model_class_path,
            'content_field': content_field,
            'filename_field': filename_field,
            'mimetype_field': mimetype_field,
            'filename': filename,
        }

    def _open(self, name, mode='rb'):
        assert mode[0] in 'rwab'

        storage_attrs = self._get_storage_attributes(name)
        model_class_path = storage_attrs['model_class_path']
        content_field = storage_attrs['content_field']
        filename_field = storage_attrs['filename_field']
        mimetype_field = storage_attrs['mimetype_field']
        filename = storage_attrs['filename']

        model_cls = self._get_model_cls(model_class_path)
        model_instance = model_cls.objects.only(
            content_field, mimetype_field
        ).get(**{filename_field: name})
        encoded_bytes = getattr(model_instance, content_field)

        _file = self._get_file_from_encoded_bytes(encoded_bytes)
        _file.filename = filename
        _file.mimetype = getattr(model_instance, mimetype_field)
        return _file

    def _save(self, name, content):
        storage_attrs = self._get_storage_attributes(name)
        model_class_path = storage_attrs['model_class_path']
        content_field = storage_attrs['content_field']
        filename_field = storage_attrs['filename_field']
        mimetype_field = storage_attrs['mimetype_field']

        model_cls = self._get_model_cls(model_class_path)
        new_filename = self._get_unique_filename(model_cls,
                                                 filename_field, name)
        encoded_bytes = self._get_encoded_bytes_from_file(content)
        mimetype = getattr(content.file, 'content_type', 'text/plain')

        model_cls.objects.create(**{
            content_field: encoded_bytes,
            filename_field: new_filename,
            mimetype_field: mimetype,
        })
        return new_filename

    def delete(self, name):
        storage_attrs = self._get_storage_attributes(name)
        model_class_path = storage_attrs['model_class_path']
        filename_field = storage_attrs['filename_field']

        model_cls = self._get_model_cls(model_class_path)
        model_cls.objects.filter(**{filename_field: name}).delete()

    def exists(self, name):
        storage_attrs = self._get_storage_attributes(name)
        model_class_path = storage_attrs['model_class_path']
        filename_field = storage_attrs['filename_field']
        filename = storage_attrs['filename']

        model_cls = self._get_model_cls(model_class_path)
        return model_cls.objects.filter(
            **{filename_field: filename}
        ).exists()

    def url(self, name):
        _url = reverse('db_file_storage.download_file')
        return _url + '?' + urlencode({'name': name})


class FixedModelDatabaseFileStorage(DatabaseFileStorage):
    """ File storage system that saves files in the database.

        Intended for use without Models' FileFields, e.g. with Form Wizards.
        Uses a fixed Model to store the all the saved files.
    """
    def __init__(self, *args, **kwargs):
        try:
            self.model_class_path = kwargs.pop('model_class_path')
            self.content_field = kwargs.pop('content_field')
            self.filename_field = kwargs.pop('filename_field')
            self.mimetype_field = kwargs.pop('mimetype_field')
        except KeyError:
            raise KeyError(
                "keyword args 'model_class_path', 'content_field', "
                "'filename_field' and 'mimetype_field' are required."
            )
        super(FixedModelDatabaseFileStorage, self).__init__(*args, **kwargs)

    def _get_storage_attributes(self, name):
        return {
            'model_class_path': self.model_class_path,
            'content_field': self.content_field,
            'filename_field': self.filename_field,
            'mimetype_field': self.mimetype_field,
            'filename': name,
        }
