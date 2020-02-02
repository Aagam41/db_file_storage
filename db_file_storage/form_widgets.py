# python
import sys
# third party
from django.utils.html import escape
from django.forms.widgets import ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget

if sys.version_info.major == 2:  # python2
    from urllib import unquote
else:  # python3
    from urllib.parse import unquote


def db_file_widget(cls):
    """Edit the download-link inner text."""

    def get_link_display(url):
        unquoted = unquote(url.split('%2F')[-1])
        if sys.version_info.major == 2:  # python 2
            from django.utils.encoding import force_unicode
            unquoted = force_unicode(unquoted)
        return escape(unquoted)

    def get_context(self, name, value, attrs):
        context = super(cls, self).get_context(name, value, attrs)
        if value and hasattr(value, 'url'):
            context['widget']['display'] = get_link_display(value.url)
        return context
    setattr(cls, 'get_context', get_context)

    return cls


@db_file_widget
class DBClearableFileInput(ClearableFileInput):
    template_name = 'db_file_storage/widgets/clearable_file_input.html'


@db_file_widget
class DBAdminClearableFileInput(AdminFileWidget):
    template_name = 'db_file_storage/widgets/admin_clearable_file_input.html'
