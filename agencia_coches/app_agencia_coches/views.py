from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *

def hola_mundo (request):
    return HttpResponse ("<h1>hola mundo</h1>")



@login_required
def dashboard (request):
    return render(request,'index.html')


# Forma para registrar un empleado en el login
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Aquí podrías crear el Employee automáticamente vinculado a este user
            Employee.objects.create(user=user, nombre=user.username)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



# Tabla de coches
@login_required
def cars (request):
    cars = Cars.objects.all()
    return render(request, 'cars/cars.html', {'cars':cars})

# Crear los coches
@login_required
def cars_create(request):
    if request.method == 'GET':
        return render(request, 'cars/cars_create.html', {'cars_form': CarsForm}) 
    
    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save()
        return redirect ('cars')
    else:
        form = CarsForm(data = request.POST)
        return render (request, 'cars/cars_create.html',{'cars_form': CarsForm})
    
@login_required
def car_detail(request, pk):
    # Busca el coche por su ID (pk) o lanza un error 404 si no existe
    car = get_object_or_404(Cars, pk=pk)
    imagenes = car.imagenes_adicionales.all()
    return render(request, 'cars/car_detail.html', {'car': car,'imagenes': imagenes})



# Tabla de trabajadores
@login_required
def employees (request):
    employees = Employee.objects.all()
    return render(request, 'employee/employees.html', {'employees':employees})

# Crear los trabajadores
@login_required
def employees_create(request):
    if request.method == 'GET':
        return render(request, 'employee/employees_create.html', {'employees_form': EmployeesForm}) 
    
    if request.method == 'POST':
        form = EmployeesForm(request.POST, request.FILES)
    
    if form.is_valid():
        # Sacamos los datos del usuario del formulario
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        # Creamos el User de Django
        user_creado = User.objects.create_user(username = username, password = password)
        
        # Guardamos el Employee vinculándolo al usuario
        employee = form.save(commit = False)
        employee.user = user_creado
        employee.nombre = username
        employee.save()

        return redirect ('employees')
    else:
        form = EmployeesForm(data = request.POST)
        return render (request, 'employee/employees_create.html',{'employees_form': EmployeesForm})

@login_required
def employee_detail(request, pk):
    # Busca el empleado por su ID (pk) o lanza un error 404 si no existe
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employee/employee_detail.html', {'employee': employee})



# Tabla de extras
@login_required
def extras (request):
    extras = Extra.objects.all()
    return render(request, 'extras/extras.html', {'extras':extras})

# Crear los extras
@login_required
def extras_create(request):
    if request.method == 'GET':
        return render(request, 'extras/extras_create.html', {'extras_form': ExtrasForm}) 
    
    if request.method == 'POST':
        form = ExtrasForm(request.POST, request.FILES)
    
    if form.is_valid():
        form.save()
        return redirect ('extras')
    else:
        form = ExtrasForm(data = request.POST)
        return render (request, 'extras/extras_create.html',{'extras_form': ExtrasForm})
    