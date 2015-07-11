# python
import sys
# django
from django.shortcuts import render
# third party
from db_file_storage.storage import FixedModelDatabaseFileStorage
from formtools.wizard.views import SessionWizardView
# project
from .forms import SongLyricsForm1, SongLyricsForm2, SongLyricsForm3


class SongLyricsWizard(SessionWizardView):
    file_storage = FixedModelDatabaseFileStorage(
        model_class_path='form_wizard_example.FormWizardTempFile',
        content_field='content',
        filename_field='name',
        mimetype_field='mimetype'
    )
    form_list = [SongLyricsForm1, SongLyricsForm2, SongLyricsForm3]
    template_name = 'form_wizard_example/form.html'

    def done(self, form_list, **kwargs):
        if sys.version_info.major == 3:  # python3
            form_list = list(form_list)
        song = form_list[0].cleaned_data['song']
        artist = form_list[0].cleaned_data['artist']
        lyrics = form_list[1].cleaned_data['attachment'].read()
        sender = form_list[2].cleaned_data['sender']

        context = {'song': song, 'artist': artist,
                   'lyrics': lyrics, 'sender': sender}
        return render(self.request, 'form_wizard_example/done.html', context)
