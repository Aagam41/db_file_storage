# third party
import django

if django.VERSION > (2,):
    from django.urls import reverse, include, reverse_lazy
    from django.urls import re_path as url
else:
    try:
        from django.core.urlresolvers import reverse, reverse_lazy
    except ImportError:
        from django.urls import reverse, reverse_lazy

__all__ = ['reverse', 'include', 'reverse_lazy', 'url']
