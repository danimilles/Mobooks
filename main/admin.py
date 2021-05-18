from django.contrib import admin

# Register your models here.
from main.models import Author, Genre, Publisher, Book

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)