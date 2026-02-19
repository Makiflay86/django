from django.contrib import admin
from django.utils.html import format_html
from .models import *



# Registros sencillos
admin.site.register(Employee)
admin.site.register(Extra)



# 1. El Inline para las fotos adicionales
class CarImagesInline(admin.TabularInline):
    model = CarImages
    extra = 10
    fields = ['imagen']



# 2. La configuración de Cars
@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('ver_miniatura', 'marca', 'modelo', 'combustible', 'kilometros')
    inlines = [CarImagesInline]

    def ver_miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 50px; height: 35px; border-radius: 5px; object-fit: cover;" />', obj.imagen.url)
        return "Sin foto"
    
    ver_miniatura.short_description = 'Vista Previa'