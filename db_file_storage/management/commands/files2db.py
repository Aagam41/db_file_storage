import argparse
import os
import re

from django.apps import apps
from django.db import models
from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand


_ = lambda x: x

DB_PATTERN = re.compile(r'^\w+\.\w+/bytes/filename/mimetype$')


class Command(BaseCommand):
    help = _("Copy separate media files from file system into database after the migration to db_file_storage.")

    def __init__(self):
        super(Command, self).__init__()
        try:
            self.MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
        except AttributeError:
            self.stderr.write(
                    'Please configure MEDIA_ROOT in your settings. '
                    'Otherwise files in standard file storage cannot be found.')

    def add_arguments(self, parser):
        parser.formatter_class = argparse.RawTextHelpFormatter
        parser.description = """
            ------------------------------------------------------------
            Copy separate media files from file system into database after the migration to db_file_storage.
            ------------------------------------------------------------
        """

    def handle(self, *args, **options):
        for app, tbl, model, fld in self.get_media_fields():
            if re.match(DB_PATTERN, fld.upload_to):
                kwargs = {
                    '{0}__exact'.format(fld.name): '',
                }
                media_files = model.objects.select_for_update().exclude(**kwargs).only(
                        model._meta.pk.name, fld.name)

                cnt_non_db = cnt_format_unknown = 0
                for media_file in media_files:
                    field_file = getattr(media_file, fld.name)
                    if not re.match(DB_PATTERN, os.path.dirname(field_file.name)):
                        cnt_non_db += 1
                        maybe_file = os.path.join(self.MEDIA_ROOT, field_file.name)
                        if os.path.isfile(maybe_file):
                            self.cp(field_file, maybe_file)
                        else:
                            cnt_format_unknown += 1
                self.report(app, tbl, fld, 'db', len(media_files), cnt_non_db, cnt_format_unknown)
            else:
                self.report(app, tbl, fld, 'other')

    @staticmethod
    def cp(field_file, media_file):
        new_name = os.path.basename(media_file)
        with open(media_file, 'rb') as f:
            field_file.save(new_name, File(f))

    def report(self, app, tbl, fld, storage, cntfiles=None, cnt_non_db=0, cnt_format_unknown=0):
        if cntfiles is not None:
            storage = '%s storage - contains %s file(s): %s std format - %s%s db format' % (
                    storage, cntfiles, cnt_non_db - cnt_format_unknown,
                    '%s unknown - ' if cnt_format_unknown else '', cntfiles - cnt_non_db)
        self.stdout.write('%s %s %s - %s' % (app.label, tbl, fld.name, storage))

    @staticmethod
    def get_media_fields():
        for app in apps.get_app_configs():
            for tbl, model in app.models.items():
                for fld in model._meta.get_fields():
                    if isinstance(fld, models.FileField):
                        yield (app, tbl, model, fld)
