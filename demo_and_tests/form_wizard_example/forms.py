# django
from django import forms


class SongLyricsForm1(forms.Form):
    song = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)


class SongLyricsForm2(forms.Form):
    attachment = forms.FileField(label='Lyrics', help_text='a plain text file')


class SongLyricsForm3(forms.Form):
    sender = forms.CharField(max_length=100)
