from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CarsForm

def hola_mundo (request):
    return HttpResponse ("<h1>hola mundo</h1>")

def home (request):
    cars = Cars.objects.all()
    return render(request,'index.html',{'cars':cars})



# Tabla de coches
def cars (request):
    cars = Cars.objects.all()
    return render(request, 'cars/preview.html', {'cars':cars})

# Crear los coches
def cars_create(request):
    if request.method == 'GET':
        return render(request, 'cars/cars_create.html', {'cars_form': CarsForm}) 
    
    if request.method == 'POST':
        form = CarsForm(data = request.POST)
    
    if form.is_valid:
        form.save()
        return redirect ('/cars/')
    else:
        form = CarsForm(data = request.POST)
        return render (request, 'cars/cars_create.html',{'cars_form': CarsForm})