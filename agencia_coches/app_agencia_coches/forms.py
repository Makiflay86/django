from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CarsForm (forms.ModelForm):

    class Meta:
        model = Cars
        fields='__all__'
        widgets = {
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'fecha_fabricacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date', 
                    'class': 'form-control',
                    'style': 'background: #fcfcfc; border-radius: 12px;'
                }
            ),
        }



class EmployeesForm(forms.ModelForm):
    username = forms.CharField(label="Nombre de usuario", max_length=150, required=False)
    # Campo obligatorio para seguridad
    old_password = forms.CharField(label="Contraseña Actual", widget=forms.PasswordInput, required=False)
    # Campo opcional para el cambio
    password = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput, required=False)

    class Meta:
        model = Employee
        fields = ['apellidos', 'puesto', 'foto']

    field_order = ['username', 'apellidos', 'old_password', 'password', 'puesto', 'foto']



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