# django
from django.conf.urls import url
# project
from .views import SongLyricsWizard


urlpatterns = [
    url(r'^song_lyrics/$', SongLyricsWizard.as_view(), name='song_lyrics'),
]
