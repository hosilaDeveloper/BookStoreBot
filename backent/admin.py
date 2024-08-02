from django.contrib import admin
from .models import Books


# Register your models here.


@admin.register(Books)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'price')
    list_display_links = ('id', 'title', 'author', 'price')
    search_fields = ('title', 'author')
