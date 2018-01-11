# -*- coding: utf-8 -*-
# python
from __future__ import unicode_literals
import os
# django
from django.conf import settings
from django.test import TestCase
# third party
from db_file_storage.storage import FixedModelDatabaseFileStorage
from db_file_storage.compat import reverse
# project
from form_wizard_example.models import FormWizardTempFile


class FormWizardTestCase(TestCase):

    def test_fixed_model_storage_requires_fixed_model_fields(self):
        with self.assertRaises(KeyError):
            FixedModelDatabaseFileStorage()

    def test_wizard_view(self):
        url = reverse('form_wizard:song_lyrics')

        # Begins with no files
        self.assertEqual(FormWizardTempFile.objects.count(), 0)

        # first step - song and artist
        form_data = {
            'song_lyrics_wizard-current_step': '0',
            '0-song': 'Californication',
            '0-artist': 'Red Hot Chili Peppers'
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)

        # second step - file
        path = os.path.join(settings.TEST_FILES_DIR, 'californication.txt')
        with open(path, 'rb') as lyric_file:
            form_data = {
                'song_lyrics_wizard-current_step': '1',
                '1-attachment': lyric_file
            }
            response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)

        # Creates a file until the wizard is complete
        self.assertEqual(FormWizardTempFile.objects.count(), 1)

        # third step - song and artist
        form_data = {
            'song_lyrics_wizard-current_step': '2',
            '2-sender': 'Victor Silva'
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['song'], 'Californication')
        self.assertEqual(response.context['artist'], 'Red Hot Chili Peppers')
        self.assertEqual(response.context['sender'], 'Victor Silva')

        some_lines = (
            b"It's the edge of the world",
            b"Dream of Californication",
            b"Marry me girl be my fairy to the world",
            b"And Alderon's not far away",
            b"Destruction leads to a very rough road",
            b"And tidal waves couldn't save the world"
        )

        for line in some_lines:
            self.assertIn(line, response.context['lyrics'])

        # Cleans the file after the wizard is complete
        self.assertEqual(FormWizardTempFile.objects.count(), 0)
