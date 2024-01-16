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

    from django.conf.urls import include
    try:
        from django.conf.urls import url
    except ImportError:
        from django.urls import path as url, include

__all__ = ['reverse', 'include', 'reverse_lazy', 'url']
