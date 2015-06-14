# django imports
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# project imports
from .forms import CDForm, SoundDeviceForm
from .models import CD, SoundDevice


urlpatterns = patterns('',
    url(
        r'^$',
        ListView.as_view(
            queryset=CD.objects.all(),
            template_name='music/cd_list.html'
        ),
        name='cd.list'
    ),
    url(
        r'^cds/add/$',
        CreateView.as_view(
            model=CD,
            form_class=CDForm,
            template_name='music/cd_form.html',
            success_url=reverse_lazy('cd.list')
        ),
        name='cd.add'
    ),
    url(
        r'^cds/edit/(?P<pk>\d+)/$',
        UpdateView.as_view(
            model=CD,
            form_class=CDForm,
            template_name='music/cd_form.html',
            success_url=reverse_lazy('cd.list')
        ),
        name='cd.edit'
    ),
    url(
        r'^cds/delete/(?P<pk>\d+)/$',
        DeleteView.as_view(
            model=CD,
            success_url=reverse_lazy('cd.list')
        ),
        name='cd.delete'
    ),
    url(
        r'^sound_devices/add/$',
        CreateView.as_view(
            model=SoundDevice,
            form_class=SoundDeviceForm,
            template_name='music/sound_device_form.html',
            success_url=reverse_lazy('cd.list')
        ),
        name='sound_device.add'
    ),
)
