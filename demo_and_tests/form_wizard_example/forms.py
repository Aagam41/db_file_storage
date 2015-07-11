# django
from django import forms


class SongLyricsForm1(forms.Form):
    song = forms.CharField(max_length=100)
    artist = forms.CharField(max_length=100)


class SongLyricsForm2(forms.Form):
    attachment = forms.FileField()


class SongLyricsForm3(forms.Form):
    sender = forms.CharField(max_length=100)
