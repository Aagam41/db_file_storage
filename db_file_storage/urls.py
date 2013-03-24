# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url


urlpatterns = patterns('db_file_storage',
    url(r'^download/', 'views.download_file', name='db_file_storage.download_file')
)
