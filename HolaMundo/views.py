from django.shortcuts import render
from django.http import HttpResponse # Necesario para poder responder al cliente
from HolaMundo.models import Author,Book

# Create your views here.

# forma de responder al cliente cuando hace un http
def hola_mundo (request): # El request captura las peticiones de los clientes
    return HttpResponse ("<h1>hola mundo</h1>")
# Con esto hemos habilitado una vista, pero hay que además enlazar el proyecto con la aplicación

def home (request): # Pinta una página con render, también hay que darlo de alta en urls.py
    author = Author.objects.all() # Añadiendo los autores
    book = Book.objects.all() # Añadiendo los libros
    return render(request,'index.html', {'authors': author, 'books': book}) # La página index.html hay que crearla dentro del archivo de configuración de todo proyecto de django, settings.py
