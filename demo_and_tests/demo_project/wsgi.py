import os
from django.core.wsgi import get_wsgi_application

# WSGI config for "Django DB File Storage"'s demo project.
# Exposes the WSGI callable as a module-level variable named ``application``.
# For more information on this file, see
# https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_project.settings")
application = get_wsgi_application()
