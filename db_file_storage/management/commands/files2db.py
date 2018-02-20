import argparse
import re

from django.apps import apps
from django.db import models
from django.core.management.base import BaseCommand


_ = lambda x: x


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
        for app, tbl, fld in self.get_media_fields():
            if re.match(r'^\w+\.\w+/bytes/filename/mimetype$', fld.upload_to):
                self.stdout.write(app.label)
                self.stdout.write(tbl)
                self.stdout.write(fld.name)
                self.stdout.write('')

    def get_media_fields(self):
        for app in apps.get_app_configs():
            for tbl, model in app.models.items():
                for fld in model._meta.get_fields():
                    if isinstance(fld, models.FileField):
                        yield (app, tbl, fld)
