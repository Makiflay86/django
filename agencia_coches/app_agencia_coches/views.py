from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib import messages # Importa los mensajes
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

@login_required
def dashboard(request):
    # Conteos totales
    total_cars = Cars.objects.count()
    total_employees = Employee.objects.count()
    
    # Últimas incorporaciones (limitado a los 5 más recientes)
    recent_cars = Cars.objects.all().order_by('-id')[:5]
    recent_employees = Employee.objects.all().order_by('-id')[:5]
    
    context = {
        'total_cars': total_cars,
        'total_employees': total_employees,
        'recent_cars': recent_cars,
        'recent_employees': recent_employees,
    }
    return render(request, 'index.html', context)



# Forma para registrar un empleado en el login
def register(request):
    if request.method == 'POST':
        form = RegistroEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Employee.objects.create(
                user=user,
                nombre=user.username,
                apellidos=form.cleaned_data.get('apellidos'),
                puesto=form.cleaned_data.get('puesto'),
                foto=form.cleaned_data.get('foto')
            )
            # Añadimos un aviso para el usuario
            messages.success(request, f'¡Bienvenido {user.username}! Tu cuenta ha sido creada. Ya puedes iniciar sesión.')
            return redirect('login')
        else:
            # Si hay errores, avisamos que algo falló
            messages.error(request, 'Hubo un error en el registro. Revisa los datos.')
    else:
        form = RegistroEmpleadoForm()
    
    return render(request, 'registration/register.html', {'form': form})



# Tabla de coches
@login_required
def cars (request):
    cars = Cars.objects.all()
    return render(request, 'cars/cars.html', {'cars':cars})

# Crear un coche
@login_required
def cars_create(request):
    # Creamos la fábrica para gestionar las 10 imágenes adicionales
    ImageFormSet = inlineformset_factory(Cars, CarImages, fields=('imagen',), extra=10)

    if request.method == 'POST':
        form = CarsForm(request.POST, request.FILES)
        formset = ImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            # Guardamos el coche y obtenemos el objeto creado
            coche = form.save()
            
            # Guardamos las imágenes del formset vinculándolas al coche
            instancias_fotos = formset.save(commit=False)
            for foto in instancias_fotos:
                foto.car = coche # Asignamos el coche recién creado
                foto.save()
                
            return redirect('cars')
    else:
        # En GET, enviamos los formularios vacíos
        form = CarsForm()
        formset = ImageFormSet()

    return render(request, 'cars/cars_create.html', {'cars_form': form,'formset': formset})

# Editar el coche
@login_required
def cars_edit(request, pk):
    car = get_object_or_404(Cars, pk=pk)
    if request.method == "POST":
        form = CarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, f"¡El {car.marca} se ha actualizado correctamente!")
            return redirect('cars')
    else:
        form = CarsForm(instance=car)
    
    return render(request, 'cars/cars_edit.html', {'form': form, 'car': car})

# Eliminar el coche
@login_required
def cars_delete(request, pk):
    car = get_object_or_404(Cars, pk=pk)
    if request.method == "POST":
        nombre_coche = f"{car.marca} {car.modelo}"
        car.delete()
        messages.warning(request, f"Vehículo {nombre_coche} eliminado del stock.")
        return redirect('cars')
    return redirect('cars') # Si alguien entra por GET, solo redirige

# Preview del coche
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
# Editar empleado
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        form = EmployeesForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            new_password = form.cleaned_data.get('password')
            user = employee.user
            
            # Si el usuario escribió algo en el campo contraseña...
            if new_password:
                try:
                    # Validamos la contraseña contra las reglas de settings.py
                    validate_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                except ValidationError as e:
                    # Si no cumple los requisitos, añadimos el error al formulario
                    form.add_error('password', e)
                    return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

            form.save()
            messages.success(request, f"Perfil de {user.username} actualizado correctamente.")
            return redirect('employees')
    else:
        # Cargamos el nombre y el username como hicimos antes
        form = EmployeesForm(instance=employee, initial={
            'username': employee.user.username,
            'nombre': employee.nombre,
        })
    
    return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

@login_required
# Eliminar empleado
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        nombre = employee.user.username
        employee.delete()
        messages.warning(request, f"El empleado {nombre} ha sido dado de baja.")
        return redirect('employees')
    return redirect('employees')

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
    