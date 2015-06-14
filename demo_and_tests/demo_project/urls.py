from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^files/', include('db_file_storage.urls')),
    url(r'^', include('music.urls')),
)
