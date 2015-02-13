# -*- coding: utf-8 -*-

# project imports
from db_file_storage.storage import DatabaseFileStorage


def delete_file_if_needed(instance, filefield_name):
    """
        When editing and the filefield is different from the previous one,
        delete the previous file (if any) from the database.
        Call this function immediately BEFORE saving the instance.
    """
    if instance.id:
        model_class = instance._base_manager.model

        # Check if there is a file for the instance in the database
        isnull_lookup = {'%s__isnull' % filefield_name: True}
        isempty_lookup = {'%s__exact' % filefield_name: ''}
        if model_class.objects.filter(pk=instance.pk).exclude(**isnull_lookup).exclude(**isempty_lookup).exists():
            old_file = getattr(model_class.objects.only(filefield_name).get(pk=instance.id), filefield_name)
        else:
            old_file = None

        # If there is a file, delete it if needed
        if old_file and old_file.name != getattr(instance, filefield_name):
            DatabaseFileStorage().delete(old_file.name)


def delete_file(instance, filefield_name):
    """
        Delete the file (if any) from the database.
        Call this function immediately AFTER deleting the instance.
    """
    file_instance = getattr(instance, filefield_name)
    if file_instance:
        DatabaseFileStorage().delete(file_instance.name)
