# django
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView


app_name = 'demo_project'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^$',
        TemplateView.as_view(template_name='home.html'),
        name='home'
    ),
    url(
        r'^files/',
        include('db_file_storage.urls')
    ),
    url(
        r'^model_files/',
        include('model_filefields_example.urls', namespace='model_files')
    ),
    url(
        r'^form_wizard/',
        include('form_wizard_example.urls', namespace='form_wizard')
    ),
]
