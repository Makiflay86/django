from django.contrib import admin

# Importamos todos los models
from .models import Employee, Extra, Cars, CarImages

admin.site.register(Employee)
admin.site.register(Extra)
admin.site.register(Cars)
admin.site.register(CarImages)
