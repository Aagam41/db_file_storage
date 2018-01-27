# project
from .views import SongLyricsWizard
from db_file_storage.compat import url


app_name = 'form_wizard_example'

urlpatterns = [
    url(r'^song_lyrics/$', SongLyricsWizard.as_view(), name='song_lyrics'),
]
