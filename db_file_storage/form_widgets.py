# -*- coding: utf-8 -*-

# python imports
import sys

# django imports
from django import VERSION as DJ_VERSION
from django.utils.encoding import python_2_unicode_compatible
from django.utils.html import escape
from django.forms.widgets import ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget

if sys.version_info.major == 2:  # python2
    from urllib import unquote
else:  # python3
    from urllib.parse import unquote


@python_2_unicode_compatible
class FakeValue(object):
    def __init__(self, value):
        self.name = value.name.split('/')[-1]
        self.url = value.url

    def __str__(self):
        return self.name


def db_file_widget(cls):
    """
        Editing the download-link inner text.
    """
    if DJ_VERSION >= (1, 8, 0, '', 0):
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
    else:
        def render(self, name, value, attrs=None):
            if value and hasattr(value, 'url'):
                render_value = FakeValue(value)
            else:
                render_value = value
            return super(cls, self).render(name, render_value, attrs)
        setattr(cls, 'render', render)
    return cls


@db_file_widget
class DBClearableFileInput(ClearableFileInput):
    pass


@db_file_widget
class DBAdminClearableFileInput(AdminFileWidget):
    pass
