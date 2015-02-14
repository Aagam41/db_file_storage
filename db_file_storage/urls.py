# -*- coding: utf-8 -*-

# django imports
from django.conf.urls import patterns, url


urlpatterns = patterns('db_file_storage',
    url(
        r'^download/',
        'views.get_file',
        {'add_attachment_headers': True},
        name='db_file_storage.download_file'
    ),
    url(
        r'^get/',
        'views.get_file',
        {'add_attachment_headers': False},
        name='db_file_storage.get_file'
    )
)
