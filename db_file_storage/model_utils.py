# -*- coding: utf-8 -*-

# project imports
from db_file_storage.storage import DatabaseFileStorage


def delete_file_if_needed(instance, filefield_name):
    """
        When editing and the filefield is a new file,
          delete the previous file (if any) from the database.
        Call this function immediately BEFORE saving the instance.
    """
    if instance.id:
        model_class = instance._base_manager.model

        # Check if there is a file for the instance in the database
        if model_class.objects.filter(pk=instance.pk).exclude(
            **{'%s__isnull' % filefield_name: True}
        ).exclude(
            **{'%s__exact' % filefield_name: ''}
        ).exists():
            old_file = getattr(
                model_class.objects.only(filefield_name).get(pk=instance.id),
                filefield_name
            )
        else:
            old_file = None

        # If there is a file, delete it if needed
        if old_file:
            # When editing and NOT changing the file,
            #   old_file.name == getattr(instance, filefield_name)
            #   returns True. In this case, the file must NOT be deleted.
            # If the file IS being changed, the comparison returns False.
            #   In this case, the old file MUST be deleted.
            if (old_file.name == getattr(instance, filefield_name)) is False:
                DatabaseFileStorage().delete(old_file.name)


def delete_file(instance, filefield_name):
    """
        Delete the file (if any) from the database.
        Call this function immediately AFTER deleting the instance.
    """
    file_instance = getattr(instance, filefield_name)
    if file_instance:
        DatabaseFileStorage().delete(file_instance.name)
