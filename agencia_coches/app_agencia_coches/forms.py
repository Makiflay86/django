from django import forms
from .models import *

class CarsForm (forms.ModelForm):

    class Meta:
        model = Cars
        fields='__all__'
