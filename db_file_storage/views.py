# -*- coding: utf-8 -*-

from db_file_storage.storage import DatabaseFileStorage
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseBadRequest


storage = DatabaseFileStorage()


def download_file(request):
    name = request.GET.get('name')
    
    try:
        dict_file = storage.open(name)
    except:
        return HttpResponseBadRequest(u'Requisição inválida.')
    
    response = HttpResponse(
        FileWrapper(dict_file['file']),
        content_type = dict_file['mimetype']
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % dict_file['filename']
    return response
    
def get_file(request):
    name = request.GET.get('name')
    
    try:
        dict_file = storage.open(name)
    except:
        return HttpResponseBadRequest(u'Requisição inválida.')
    
    response = HttpResponse(
        FileWrapper(dict_file['file']),
        content_type = dict_file['mimetype']
    )
    return response
    
