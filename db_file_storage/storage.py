"""Custom Django FILE_STORAGE that saves files in the database."""

# python
import base64
import os
# third party
from django.apps import apps
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.db.models import BinaryField
from django.utils.crypto import get_random_string
from django.utils.http import urlencode
from django.utils.deconstruct import deconstructible
# project
from .compat import reverse


NAME_FORMAT_HINT = '<app>.<model>/<content_field>/<mimetype_field>' \
                   '/<filename_field>/<filename>'


class NameException(Exception):
    pass


@deconstructible
class DatabaseFileStorage(Storage):
    """File storage system that saves models' FileFields in the database.

    Intended for use with Models' FileFields.
    Uses a specific model for each FileField of each Model.
    """

    def _get_model_cls(self, model_class_path):
        app_label, model_name = model_class_path.rsplit('.', 1)
        return apps.get_model(app_label, model_name)

    def _get_encoded_bytes_from_file(self, content_field, _file):
        _file.seek(0)
        file_content = _file.read()
        encoded = base64.b64encode(file_content)
        if isinstance(content_field, BinaryField):
            return encoded
        return encoded.decode('utf-8')

    def _get_file_from_encoded_bytes(self, encoded_bytes):
        file_buffer = base64.b64decode(encoded_bytes)
        return ContentFile(file_buffer)

    def _get_unique_filename(self, model_cls, filename_field, filename):
        final_name = filename

        if ('.' in filename.rsplit(os.sep, 1)[-1]):
            stem, extension = final_name.rsplit('.', 1)
        else:
            stem, extension = (final_name, '')

        random_str = get_random_string(7)
        while model_cls.objects.filter(
            **{filename_field: final_name}
        ).exists():  # pragma: no cover
            final_name = '%s_(%s)%s' % (
                stem, random_str,
                ('.%s' % extension) if extension else ''
            )
            random_str = get_random_string(7)
        return final_name

    def _get_storage_attributes(self, name):
        if os.sep != '/':  # Windows fix (see a6d4707) # pragma: no cover
            name = name.replace('/', os.sep)
        try:
            (
                model_class_path,
                content_field,
                filename_field,
                mimetype_field,
                filename
            ) = name.split(os.sep)
        except ValueError:
            raise NameException(
                'Wrong name format. Got {} ; should be {}'.format(
                    name, NAME_FORMAT_HINT)
            )
        return {
            'model_class_path': model_class_path,
            'content_field': content_field,
            'filename_field': filename_field,
            'mimetype_field': mimetype_field,
            'filename': filename,
        }

    def _open(self, name, mode='rb'):
        assert mode[0] in 'rwab'

        if os.sep != '/':  # Windows fix (see a6d4707) # pragma: no cover
            name = name.replace('/', os.sep)

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
        content_field_name = storage_attrs['content_field']
        filename_field_name = storage_attrs['filename_field']
        mimetype_field_name = storage_attrs['mimetype_field']

        model_cls = self._get_model_cls(model_class_path)
        new_filename = self._get_unique_filename(model_cls, filename_field_name, name)

        content_field = model_cls._meta.get_field(content_field_name)
        encoded_bytes = self._get_encoded_bytes_from_file(content_field, content)

        mimetype = (
            getattr(content, 'content_type', None) or  # Django >= 1.11
            getattr(content.file, 'content_type', None) or  # Django < 1.11
            'text/plain'  # Fallback
        )

        model_cls.objects.create(**{
            content_field_name: encoded_bytes,
            filename_field_name: new_filename,
            mimetype_field_name: mimetype,
        })
        return new_filename

    def delete(self, name):
        if os.sep != '/':  # Windows fix (see a6d4707) # pragma: no cover
            name = name.replace('/', os.sep)
        storage_attrs = self._get_storage_attributes(name)
        model_class_path = storage_attrs['model_class_path']
        filename_field = storage_attrs['filename_field']

        model_cls = self._get_model_cls(model_class_path)
        model_cls.objects.filter(**{filename_field: name}).delete()

    def exists(self, name):
        if os.sep != '/':  # Windows fix (see a6d4707) # pragma: no cover
            name = name.replace('/', os.sep)
        try:
            storage_attrs = self._get_storage_attributes(name)
        except NameException:
            return False
        model_class_path = storage_attrs['model_class_path']
        filename_field = storage_attrs['filename_field']

        model_cls = self._get_model_cls(model_class_path)
        return model_cls.objects.filter(
            **{filename_field: name}
        ).exists()

    def url(self, name):
        _url = reverse('db_file_storage.download_file')
        return _url + '?' + urlencode({'name': name})


class FixedModelDatabaseFileStorage(DatabaseFileStorage):
    """File storage system that saves files in the database.

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
