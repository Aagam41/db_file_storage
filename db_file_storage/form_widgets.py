# python
import sys
# django
from django.utils.html import escape
from django.forms.widgets import ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget

if sys.version_info.major == 2:  # python2
    from urllib import unquote
else:  # python3
    from urllib.parse import unquote


def db_file_widget(cls):
    """Edit the download-link inner text."""
    def get_template_substitution_values(self, value):
        subst = super(cls, self).get_template_substitution_values(value)
        unquoted = unquote(value.url.split('%2F')[-1])
        if sys.version_info.major == 2:  # python 2
            from django.utils.encoding import force_unicode
            unquoted = force_unicode(unquoted)
        subst['initial'] = escape(unquoted)
        return subst
    setattr(
        cls,
        'get_template_substitution_values',
        get_template_substitution_values
    )
    return cls


@db_file_widget
class DBClearableFileInput(ClearableFileInput):
    pass


@db_file_widget
class DBAdminClearableFileInput(AdminFileWidget):
    pass
