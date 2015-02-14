# -*- coding: utf-8 -*-

# django imports
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _

# project imports
from db_file_storage.storage import DatabaseFileStorage


storage = DatabaseFileStorage()


def get_file(request, add_attachment_headers):
    name = request.GET.get('name')

    try:
        dict_file = storage.open(name)
    except:
        return HttpResponseBadRequest(_('Invalid request'))

    response = HttpResponse(
        FileWrapper(dict_file['file']),
        content_type=dict_file['mimetype']
    )

    if add_attachment_headers:
        response['Content-Disposition'] = \
            'attachment; filename=%s' % dict_file['filename']

    return response
