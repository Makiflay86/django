from django.shortcuts import render
from django.http import HttpResponse # Necesario para poder responder al cliente
from HolaMundo.models import Author,Book
from HolaMundo.forms import AutorForm

# Create your views here.

# forma de responder al cliente cuando hace un http
def hola_mundo (request): # El request captura las peticiones de los clientes
    return HttpResponse ("<h1>hola mundo</h1>")
# Con esto hemos habilitado una vista, pero hay que además enlazar el proyecto con la aplicación

def home (request): # Pinta una página con render, también hay que darlo de alta en urls.py
    return render(request,'index.html') # La página index.html hay que crearla dentro del archivo de configuración de todo proyecto de django, settings.py

def author (request):
    author = Author.objects.all()
    return render(request,'author.html',{'authors': author})

def author_create(request):
    return render(request,'author_create.html',{'author_form': AutorForm})

def book (request):
    book = Book.objects.all()
    return render(request,'book.html',{'books': book})

def book_create(request):
    return render(request,'book_create.html')