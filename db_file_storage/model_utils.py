# -*- coding: utf-8 -*-

from db_file_storage.storage import DatabaseFileStorage


def delete_file_if_needed(instance, filefield_name):
    """
        When editing and the filefield is different from the previous one,
        delete the previous file (if any) from the database.
    """
    if instance.id:
        ModelClass = instance._base_manager.model
        
        isnull_lookup = {'%s__isnull' % filefield_name: True}
        isempty_lookup = {'%s__exact' % filefield_name: ''}
        if ModelClass.objects.filter(pk=instance.pk).exclude(**isnull_lookup).exclude(**isempty_lookup).exists():
            old_file = getattr(ModelClass.objects.only(filefield_name).get(pk=instance.id), filefield_name)
        else:
            old_file = None
        
        if old_file and old_file.name != getattr(instance, filefield_name):
            DatabaseFileStorage().delete(old_file.name)