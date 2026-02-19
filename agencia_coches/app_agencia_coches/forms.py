from django import forms
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
