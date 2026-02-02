from django.contrib import admin
from HolaMundo.models import Author, Book

# Register your models here.

#Forma de registrar la tabla Author
admin.site.register(Author)

#Registramos la tabla Book
admin.site.register(Book)