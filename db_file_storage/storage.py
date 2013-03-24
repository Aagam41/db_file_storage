# -*- coding: utf-8 -*-

from cStringIO import StringIO
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
from importlib import import_module
from urllib import urlencode


def _get_model_class(model_class_path):
    app_module_name, model_class_name = model_class_path.rsplit('.', 1)
    models_module = import_module('%s.models' % app_module_name)
    return getattr(models_module, model_class_name)
    

def _get_encoded_bytes_from_file(file):
    file.seek(0)
    return file.read().encode('base64')


def _get_file_from_encoded_bytes(encoded_bytes):
    file_buffer = str(encoded_bytes).decode('base64')
    return StringIO(file_buffer)
    

def _get_unique_filename(Model, filename_field, filename):
    final_name = filename
    stem, ext = final_name.rsplit('.', 1) if ('.' in final_name) else (final_name, '')
    append_to_name = 1
    while Model.objects.filter(**{filename_field: final_name}).exists():
        final_name = '%s_(%s)%s' % (
            stem,
            append_to_name,
            ('.%s' % ext) if ext else ''
        )
        append_to_name += 1
    return final_name


class DatabaseFileStorage(Storage):
    
    def _open(self, name, mode='rb'):
        model_class_path, content_field, filename_field, mimetype_field, filename = name.split('/')
        Model = _get_model_class(model_class_path)
        model_instance = Model.objects.only(content_field, mimetype_field).get(**{filename_field: name})
        encoded_bytes = getattr(model_instance, content_field)
        return {
            'filename': filename,
            'file': _get_file_from_encoded_bytes(encoded_bytes),
            'mimetype': getattr(model_instance, mimetype_field)
        }
    
    
    def _save(self, name, content):
        model_class_path, content_field, filename_field, mimetype_field, filename = name.split('/')
        Model = _get_model_class(model_class_path)
        new_filename = _get_unique_filename(Model, filename_field, name)
        encoded_bytes = _get_encoded_bytes_from_file(content)
        mimetype = content.file.content_type
        
        Model.objects.create(**{
            content_field: encoded_bytes,
            filename_field: new_filename,
            mimetype_field: mimetype,
        })        
        
        return new_filename
    
    
    def delete(self, name):
        model_class_path, content_field, filename_field, mimetype_field, filename = name.split('/')
        Model = _get_model_class(model_class_path)
        Model.objects.filter(**{filename_field: name}).delete()
    
    
    def exists(self, name):
        model_class_path, content_field, filename_field, mimetype_field, filename = name.split('/')
        Model = _get_model_class(model_class_path)
        return Model.objects.filter(**{filename_field: filename}).exists()
    
    
    def url(self, name):
        _url = reverse('db_file_storage.download_file')
        return _url + '?' + urlencode({'name': name})

