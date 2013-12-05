# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('db_file_storage',
    url(r'^download/', 'views.download_file', name='db_file_storage.download_file'),
    url(r'^get/', 'views.download_file', {'add_attachment_headers': False}, name='db_file_storage.get_file')
)
