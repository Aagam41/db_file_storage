# -*- coding: utf-8 -*-

# python imports
from urllib import unquote

# django imports
from django import VERSION
from django.utils.encoding import force_unicode, force_text, python_2_unicode_compatible
from django.utils.html import escape
from django.forms.widgets import ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget


def db_file_widget(cls):
    """
        Editing the download-link inner text.
    """
    if VERSION >= (1, 8, 0, '', 0):
        def get_template_substitution_values(self, value):
            subst = super(cls, self).get_template_substitution_values(value)
            subst['initial'] = escape(force_unicode(unquote(value.url.split('%2F')[-1])))
            return subst
        setattr(cls, 'get_template_substitution_values', get_template_substitution_values)
    else:
        def render(self, name, value, attrs=None):
            if hasattr(value, 'url'):
                @python_2_unicode_compatible
                class FakeValue:
                    def __init__(self2, value):
                        self2.name = value.name.split('/')[-1]
                        self2.url = value.url

                    def __str__(self2):
                        return self2.name

            else:
                def FakeValue(value):
                    return value
            return super(cls, self).render(name, FakeValue(value), attrs)
        setattr(cls, 'render', render)
    return cls


@db_file_widget
class DBClearableFileInput(ClearableFileInput):
    pass


@db_file_widget
class DBAdminClearableFileInput(AdminFileWidget):
    pass
