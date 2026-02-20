from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib import messages # Importa los mensajes
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash

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
        
        # 1. Gestionar eliminación de imágenes existentes del servidor
        imagenes_a_borrar = request.POST.getlist('borrar_imagenes')
        if imagenes_a_borrar:
            # Esto elimina el registro y, dependiendo de tu config, el archivo físico
            car.imagenes_adicionales.filter(id__in=imagenes_a_borrar).delete()
            
        if form.is_valid():
            form.save()
            
            # 2. Gestionar subida de nuevas imágenes adicionales
            nuevas_fotos = request.FILES.getlist('nuevas_imagenes')
            for foto in nuevas_fotos:
                CarImages.objects.create(car=car, imagen=foto)
            
            messages.success(request, f"¡El {car.marca} y su galería se han actualizado correctamente!")
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
        
        # 1. Extraemos las claves del POST
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password') # o 'new_password' según tu forms.py
        user = employee.user

        # 2. Seguridad: Validar contraseña actual antes de validar el form
        if not old_password or not user.check_password(old_password):
            form.add_error('old_password', 'La contraseña actual no es correcta.')
            return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

        if form.is_valid():
            # 3. Si quiere cambiar a una nueva contraseña
            if new_password:
                try:
                    validate_password(new_password, user)
                    user.set_password(new_password)
                    user.save()
                    # Importante: actualiza la sesión para que no se desloguee si es él mismo
                    update_session_auth_hash(request, user) 
                except ValidationError as e:
                    form.add_error('password', e)
                    return render(request, 'employee/employee_edit.html', {'form': form, 'employee': employee})

            # 4. Guardar cambios de username y datos de Employee
            new_username = form.cleaned_data.get('username')
            if new_username:
                user.username = new_username
                user.save()

            form.save()
            messages.success(request, f"Perfil de {user.username} actualizado.")
            return redirect('employees')
    else:
        form = EmployeesForm(instance=employee, initial={
            'username': employee.user.username,
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

# Editar extra
@login_required
def extras_edit(request, pk):
    extra = get_object_or_404(Extra, pk=pk)
    if request.method == 'POST':
        form = ExtrasForm(request.POST, instance=extra)
        if form.is_valid():
            form.save()
            return redirect('extras')
    else:
        form = ExtrasForm(instance=extra)
    return render(request, 'extras/extras_edit.html', {'form': form, 'extra': extra})

# Eliminar extra
@login_required
def extras_delete(request, pk):
    if request.method == 'POST':
        extra = get_object_or_404(Extra, pk=pk)
        extra.delete()
    return redirect('extras')