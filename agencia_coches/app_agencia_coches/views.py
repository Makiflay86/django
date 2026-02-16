from django.shortcuts import render, redirect, get_object_or_404
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
    
def car_detail(request, pk):
    # Busca el coche por su ID (pk) o lanza un error 404 si no existe
    car = get_object_or_404(Cars, pk=pk)
    return render(request, 'cars/car_detail.html', {'car': car})



# Tabla de trabajadores
def employee (request):
    employees = Employee.objects.all()
    return render(request, 'employee/employee.html', {'employees':employees})

def employee_detail(request, pk):
    # Busca el empleado por su ID (pk) o lanza un error 404 si no existe
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/employee_detail.html', {'employee': employee})
