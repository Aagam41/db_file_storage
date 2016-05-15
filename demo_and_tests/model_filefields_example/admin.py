# django
from django.contrib import admin
# project
from .forms import BookAdminForm
from .models import Book


class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm


admin.site.register(Book, BookAdmin)
