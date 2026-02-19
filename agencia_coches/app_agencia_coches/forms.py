from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CarsForm (forms.ModelForm):

    class Meta:
        model = Cars
        fields='__all__'



class EmployeesForm (forms.ModelForm):

    # Añadimos campos que NO están en el modelo Employee pero queremos en el form
    username = forms.CharField(label="Nombre de usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['apellidos', 'puesto', 'foto']

    # Ordenando la salida del formulario
    field_order = ['username', 'apellidos', 'password', 'puesto', 'foto']



class ExtrasForm (forms.ModelForm):

    class Meta:
        model = Extra
        fields='__all__'



class RegistroEmpleadoForm(UserCreationForm):
    # Añadimos los campos extra de tu modelo Employee
    apellidos = forms.CharField(max_length=100)
    puesto = forms.CharField(max_length=100)
    foto = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        # Mantenemos los campos de User y añadimos los nuevos
        fields = UserCreationForm.Meta.fields + ('apellidos', 'puesto', 'foto',)