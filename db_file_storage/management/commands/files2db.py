import argparse
import os
import re

from django.apps import apps
from django.db import models
from django.core.management.base import BaseCommand


_ = lambda x: x

DB_PATTERN = re.compile(r'^\w+\.\w+/bytes/filename/mimetype$')


class Command(BaseCommand):
    help = _("Copy separate media files from file system into database after the migration to db_file_storage.")

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
                    '{0}__gt'.format(fld.name): '',
                }
                qs_files = model.objects.select_for_update().filter(**kwargs).only(
                        model._meta.pk.name, fld.name)

                cnt_format_db = 0
                for qs_file in qs_files:
                    field_file = getattr(qs_file, fld.name)
                    if re.match(DB_PATTERN, os.path.dirname(field_file.name)):
                        cnt_format_db += 1
                self.report(app, tbl, fld, 'db', len(qs_files), cnt_format_db)
            else:
                self.report(app, tbl, fld, 'other')

    def report(self, app, tbl, fld, storage, cntfiles=None, cnt_format_db=0):
        if cntfiles is not None:
            storage = '%s - %s file(s) - %s std format - %s unknown - %s db format' % (
                    storage, cntfiles, cntfiles - cnt_format_db, 0, cnt_format_db)
        self.stdout.write('%s %s %s - %s' % (app.label, tbl, fld.name, storage))

    def get_media_fields(self):
        for app in apps.get_app_configs():
            for tbl, model in app.models.items():
                for fld in model._meta.get_fields():
                    if isinstance(fld, models.FileField):
                        yield (app, tbl, model, fld)
