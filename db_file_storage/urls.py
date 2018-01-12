# project
from db_file_storage import views
from db_file_storage.compat import url

# app_name = 'db_file_storage'

urlpatterns = [
    url(r'^download/', views.get_file, {'add_attachment_headers': True},
        name='db_file_storage.download_file'),
    url(r'^get/', views.get_file, {'add_attachment_headers': False},
        name='db_file_storage.get_file')
]
