# django imports
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# project imports
from .forms import BookForm, SoundDeviceForm
from .models import Book, SoundDevice
from db_file_storage.compat import url, reverse_lazy


app_name = 'model_filefields_example'

urlpatterns = [
    url(
        r'^$',
        ListView.as_view(
            queryset=Book.objects.all(),
            template_name='model_filefields_example/book_list.html'
        ),
        name='book.list'
    ),
    url(
        r'^books/add/$',
        CreateView.as_view(
            model=Book,
            form_class=BookForm,
            template_name='model_filefields_example/book_form.html',
            success_url=reverse_lazy('model_files:book.list')
        ),
        name='book.add'
    ),
    url(
        r'^books/edit/(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=Book,
            form_class=BookForm,
            template_name='model_filefields_example/book_form.html',
            success_url=reverse_lazy('model_files:book.list')
        ),
        name='book.edit'
    ),
    url(
        r'^books/delete/(?P<pk>\d+)/$',
        DeleteView.as_view(
            model=Book,
            success_url=reverse_lazy('model_files:book.list')
        ),
        name='book.delete'
    ),
    url(
        r'^sound_devices/add/$',
        CreateView.as_view(
            model=SoundDevice,
            form_class=SoundDeviceForm,
            template_name='model_filefields_example/sound_device_form.html',
            success_url=reverse_lazy('model_files:book.list')
        ),
        name='sound_device.add'
    ),
]
