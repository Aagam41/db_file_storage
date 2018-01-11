# -*- coding: utf-8 -*-
# python
from __future__ import unicode_literals
import mimetypes
import os
import sys
# django
from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase
from django.utils.http import urlencode
# project
from .forms import BookForm, BookAdminForm
from .models import Book, BookIndex, BookPages, SoundDevice
# third party
from db_file_storage.compat import reverse


def get_file_path(file_name):
    return os.path.join(settings.TEST_FILES_DIR, file_name)


class AddEditAndDeleteBooksTestCase(TestCase):

    def test_download_with_invalid_name(self):
        # Create book
        save_url = reverse('model_files:book.add')
        index_file = open(get_file_path('inferno_index.txt'))
        form_data = {'name': 'Inferno',
                     'index': index_file}
        self.client.post(save_url, form_data, follow=True)
        index_file.close()
        book = Book.objects.get(name='Inferno')

        # Valid name
        download_url = reverse('db_file_storage.download_file')
        download_url += '?' + urlencode({'name': str(book.index)})
        response = self.client.get(download_url)
        self.assertEqual(response.status_code, 200)

        # Invalid name
        download_url = reverse('db_file_storage.download_file')
        download_url += '?' + urlencode({'name': 'invalid_name'})
        response = self.client.get(download_url)
        self.assertEqual(response.status_code, 400)

    def test_form_widget_shows_proper_filename(self):
        # Create book
        save_url = reverse('model_files:book.add')
        index_file = open(get_file_path('inferno_index.txt'))
        form_data = {'name': 'Inferno',
                     'index': index_file}
        self.client.post(save_url, form_data, follow=True)
        index_file.close()
        book = Book.objects.get(name='Inferno')

        # Check widget download text
        form = BookForm(instance=book)
        self.assertIn('>inferno_index.txt</a>', form['index'].as_widget())

    def test_admin_form_widget_shows_proper_filename(self):
        # Create book
        save_url = reverse('model_files:book.add')
        index_file = open(get_file_path('inferno_index.txt'))
        form_data = {'name': 'Inferno',
                     'index': index_file}
        self.client.post(save_url, form_data, follow=True)
        index_file.close()
        book = Book.objects.get(name='Inferno')

        # Check widget download text
        form = BookAdminForm(instance=book)
        self.assertIn('>inferno_index.txt</a>', form['index'].as_widget())

    def test_form_widget_with_no_value(self):
        form = BookForm()
        form['index'].as_widget()
        admin_form = BookAdminForm()
        admin_form['index'].as_widget()

    def verify_file(self, download_url, file_name):
        response = self.client.get(download_url)
        with open(get_file_path(file_name), 'rb') as the_file:
            # Assert that the contents of the saved file are correct
            self.assertEqual(the_file.read(), response.content)
        # Assert that the mimetype of the saved file is correct
        self.assertEqual(
            mimetypes.guess_type(file_name)[0],
            response['Content-Type']
        )

    def test_files_operations(self):
        save_new_url = reverse('model_files:book.add')
        download_url = reverse('db_file_storage.download_file')

        #
        # Add "Inferno" book without index or pages.
        #
        form_data = {'name': 'Inferno'}
        self.client.post(save_new_url, form_data, follow=True)
        inferno = Book.objects.get(name='Inferno')
        edit_inferno_url = reverse('model_files:book.edit',
                                   kwargs={'pk': inferno.pk})
        # Assert book file fields are empty
        self.assertEqual(inferno.index.name, '')
        self.assertEqual(inferno.pages.name, '')
        # Assert no BookIndex and no BookPages were created
        self.assertEqual(BookIndex.objects.count(), 0)
        self.assertEqual(BookPages.objects.count(), 0)

        #
        # Edit Inferno: add index file
        #
        form_data = {'name': 'Inferno',
                     'index': open(get_file_path('inferno_index.txt'))}
        self.client.post(edit_inferno_url, form_data, follow=True)
        inferno = Book.objects.get(name='Inferno')
        # Assert that only a BookIndex was created
        self.assertEqual(BookIndex.objects.count(), 1)
        self.assertEqual(BookPages.objects.count(), 0)
        # Verify Inferno's new index
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')
        # Assert Inferno's pages field is still empty
        self.assertEqual(inferno.pages.name, '')

        #
        # Edit Inferno: add pages file
        #
        form_data = {'name': 'Inferno',
                     'pages': open(get_file_path('inferno_pages_v1.txt'))}
        self.client.post(edit_inferno_url, form_data, follow=True)
        inferno = Book.objects.get(name='Inferno')
        # Assert that only a BookPages was created
        self.assertEqual(BookIndex.objects.count(), 1)
        self.assertEqual(BookPages.objects.count(), 1)
        # Verify Inferno's index file is still correct
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')
        # Verify Inferno's new pages
        url = download_url + '?' + urlencode({'name': inferno.pages.name})
        self.verify_file(url, 'inferno_pages_v1.txt')

        #
        # Edit Inferno: change pages file
        #
        form_data = {'name': 'Inferno',
                     'pages': open(get_file_path('inferno_pages_v2.txt'))}
        self.client.post(edit_inferno_url, form_data, follow=True)
        inferno = Book.objects.get(name='Inferno')
        # Assert that old BookPages was deleted and new one was created
        self.assertEqual(BookIndex.objects.count(), 1)
        self.assertEqual(BookPages.objects.count(), 1)
        # Verify Inferno's index file is still correct
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')
        # Verify Inferno's new pages
        url = download_url + '?' + urlencode({'name': inferno.pages.name})
        self.verify_file(url, 'inferno_pages_v2.txt')

        #
        # Edit Inferno: clear pages file
        #
        form_data = {'name': 'Inferno',
                     'pages-clear': 'on'}
        self.client.post(edit_inferno_url, form_data, follow=True)
        inferno = Book.objects.get(name='Inferno')
        # Assert that the BookPages was deleted
        self.assertEqual(BookIndex.objects.count(), 1)
        self.assertEqual(BookPages.objects.count(), 0)
        # Assert that Inferno's pages field is empty now
        self.assertEqual(inferno.pages.name, '')
        # Assert that the contents of old Inferno's index are still correct
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')

        #
        # Add "Lost Symbol" book with index and pages.
        #
        form_data = {'name': 'Lost Symbol',
                     'index': open(get_file_path('lost_symbol_index.txt')),
                     'pages': open(get_file_path('lost_symbol_pages_v1.txt'))}
        self.client.post(save_new_url, form_data, follow=True)
        lost_symbol = Book.objects.get(name='Lost Symbol')
        inferno = Book.objects.get(name='Inferno')
        edit_lost_symbol_url = reverse('model_files:book.edit',
                                       kwargs={'pk': lost_symbol.pk})
        # Assert that one BookIndex and one BookPages were created
        self.assertEqual(BookIndex.objects.count(), 2)
        self.assertEqual(BookPages.objects.count(), 1)

        # From now on, after each change in any of the Books,
        # we check if the files are correct for both of them,
        # to ensure that saving/deleting files of a Book doesn't
        # interfere with the files of the other one.

        # Assert Infernos's page field is still empty
        self.assertEqual(inferno.pages.name, '')
        # Assert that the contents of Inferno's index are still correct
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')
        # Assert that the contents of Lost Symbol's index are correct
        url = download_url + '?' + urlencode({'name': lost_symbol.index.name})
        self.verify_file(url, 'lost_symbol_index.txt')
        # Assert that the contents of Lost Symbol's pages are correct
        url = download_url + '?' + urlencode({'name': lost_symbol.pages.name})
        self.verify_file(url, 'lost_symbol_pages_v1.txt')

        #
        # Edit Lost Symbol: clear index file
        #
        form_data = {'name': 'Lost Symbol',
                     'index-clear': 'on'}
        self.client.post(edit_lost_symbol_url, form_data, follow=True)
        lost_symbol = Book.objects.get(name='Lost Symbol')
        inferno = Book.objects.get(name='Inferno')
        # Assert one BookIndex was deleted
        self.assertEqual(BookIndex.objects.count(), 1)
        self.assertEqual(BookPages.objects.count(), 1)
        # Assert that the contents of Lost Symbol's pages are still correct
        url = download_url + '?' + urlencode({'name': lost_symbol.pages.name})
        self.verify_file(url, 'lost_symbol_pages_v1.txt')
        # Assert that the contents of Inferno's index are still correct
        url = download_url + '?' + urlencode({'name': inferno.index.name})
        self.verify_file(url, 'inferno_index.txt')
        # Assert that Inferno's pages are still empty
        self.assertEqual(inferno.pages.name, '')
        # Assert that Lost Symbol's index is empty now
        self.assertEqual(lost_symbol.index.name, '')

        #
        # Delete Inferno
        #
        inferno.delete()
        lost_symbol = Book.objects.get(name='Lost Symbol')
        # Assert one BookIndex was deleted
        self.assertEqual(BookIndex.objects.count(), 0)
        self.assertEqual(BookPages.objects.count(), 1)
        # Assert that the contents Lost Symbol's pages are still correct
        url = download_url + '?' + urlencode({'name': lost_symbol.pages.name})
        self.verify_file(url, 'lost_symbol_pages_v1.txt')
        # Assert that Lost Symbol's index is still empty
        self.assertEqual(lost_symbol.index.name, '')
        return

        #
        # Delete Lost Symbol
        #
        lost_symbol.delete()
        # Assert that there are no BookIndex or BookPages left
        self.assertEqual(BookIndex.objects.count(), 0)
        self.assertEqual(BookPages.objects.count(), 0)

    def test_binary_file(self):
        save_new_url = reverse('model_files:book.add')
        download_url = reverse('db_file_storage.download_file')

        # Save book
        form_data = {'name': 'Book With Cover',
                     'cover': open(get_file_path('book.png'), 'rb')}
        self.client.post(save_new_url, form_data, follow=True)
        book = Book.objects.get(name='Book With Cover')

        # Verify book's cover
        url = download_url + '?' + urlencode({'name': book.cover.name})
        self.verify_file(url, 'book.png')

    def test_send_same_file_for_different_rows(self):
        url = reverse('model_files:book.add')

        index_file = open(get_file_path('inferno_index.txt'))
        form_data = {'name': 'Inferno 1',
                     'index': index_file}
        self.client.post(url, form_data)
        index_file.seek(0)
        form_data = {'name': 'Inferno 2',
                     'index': index_file}
        self.client.post(url, form_data)
        index_file.close()

        self.assertEqual(BookIndex.objects.count(), 2)

        inferno_1 = Book.objects.get(name='Inferno 1')
        inferno_2 = Book.objects.get(name='Inferno 2')
        self.assertNotEqual(inferno_1.index.name, inferno_2.index.name)

    def test_file_with_no_extension(self):
        url = reverse('model_files:book.add')

        with open(get_file_path('file_without_extension')) as pages_file:
            form_data = {
                'name': 'A Random Book',
                'pages': pages_file
            }
            self.client.post(url, form_data)

        book = Book.objects.get(name='A Random Book')
        self.assertTrue(book.pages.name.endswith('/file_without_extension'))

    def test_same_file_with_no_extension_for_different_rows(self):
        url = reverse('model_files:book.add')

        index_file = open(get_file_path('file_without_extension'))
        form_data = {'name': 'Book ABC',
                     'index': index_file}
        self.client.post(url, form_data)
        index_file.seek(0)
        form_data = {'name': 'Book XYZ',
                     'index': index_file}
        self.client.post(url, form_data)
        index_file.close()

        self.assertEqual(BookIndex.objects.count(), 2)

        abc = Book.objects.get(name='Book ABC')
        xyz = Book.objects.get(name='Book XYZ')
        self.assertNotEqual(abc.index.name, xyz.index.name)

    def test_save_file_without_using_form(self):
        file_name = 'manual.txt'
        file_content_string = b'Test file content'
        content_file = ContentFile(file_content_string)

        device = SoundDevice(name='BXPM 778')
        device.instruction_manual.save(file_name, content_file)
        device.save()
        device_id = device.id

        saved_device = SoundDevice.objects.get(id=device_id)
        saved_device.instruction_manual.open('r')
        saved_device_file_content_string = \
            saved_device.instruction_manual.read()
        saved_device.instruction_manual.close()

        self.assertEqual(
            file_content_string,
            saved_device_file_content_string
        )

    def test_save_file_with_accents_without_using_form(self):
        file_name = 'manual.txt'
        if sys.version_info.major == 2:  # python2
            file_content_string = 'Accents: áãüí'.encode('utf-8')
        else:  # python3
            file_content_string = bytearray('Accents: áãüí', 'utf-8')
        content_file = ContentFile(file_content_string)

        device = SoundDevice(name='BXPM 778')
        device.instruction_manual.save(file_name, content_file)
        device.save()

        saved_device = SoundDevice.objects.get()
        saved_device.instruction_manual.open('r')
        saved_device_file_content_string = \
            saved_device.instruction_manual.read()
        saved_device.instruction_manual.close()

        self.assertEqual(
            file_content_string,
            saved_device_file_content_string
        )

    def test_storage_method_exists(self):
        self.assertFalse(default_storage.exists('file_with_wrong_name'))

        content_file = ContentFile(b'test content')
        device = SoundDevice(name='test_device')
        device.instruction_manual.save('test_file', content_file)
        device.save()

        saved_device = SoundDevice.objects.get()
        file_name = saved_device.instruction_manual.name
        self.assertTrue(default_storage.exists(file_name))

        saved_device.instruction_manual.delete()
        self.assertFalse(default_storage.exists(file_name))
