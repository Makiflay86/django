from django.db import models
from datetime import date
from django.contrib.auth.models import User


# Tabla empleado
class Employee (models.Model):

    # Esto es para que el usuario pueda logearse
    user = models.OneToOneField(
        User, 
        on_delete = models.CASCADE, 
        null = True, 
        blank = True
    )

    # Nombre
    nombre = models.CharField (
        verbose_name = 'Nombre', 
        max_length = 100,
        default = ''
    )

    # Apellidos
    apellidos = models.CharField (
        verbose_name = 'Apellidos', 
        max_length = 100,
        default = ''
    )

    # Puesto de trabajo (ej: vendedor, gerente, etc.)
    puesto = models.CharField (
        verbose_name = 'Puesto', 
        max_length = 100,
        default = ''
    )

    # Fecha de contratación
    fecha_contratacion = models.DateField (
        verbose_name = 'Fecha de contratacion', 
        auto_now_add = True
    )

    # Foto del empleado
    foto = models.ImageField (
        verbose_name = 'Foto',
        upload_to = "empleados/",
        blank = True, 
        null = True
    )

    def __str__(self):
        return self.nombre + " " + self.apellidos + " | " + self.puesto       



# Tabla extra (ej: techo solar)
class Extra(models.Model):

    nombre = models.CharField(
        max_length = 100,
        default = ''
    )

    def __str__(self):
        return self.nombre



# Tabla coches
class Cars (models.Model):

    # Marca (ej: Audi)
    marca = models.CharField (
        verbose_name = 'Marca', 
        max_length = 100,
        default = ''
    )

    # Modelo (ej: A5)
    modelo = models.CharField (
        verbose_name = 'Modelo', 
        max_length =  100,
        default = ''
    )
    
    # Fecha de fabricación
    fecha_fabricacion = models.DateField (
        verbose_name = 'Fecha de fabricacion', 
        default = date.today
    )

    # Kilómetros
    kilometros = models.PositiveIntegerField (
        verbose_name = 'Kilometros', 
        default = 0
    )

    # Combustible
    combustible = models.CharField (
        verbose_name = 'Combustible', 
        max_length = 100,
        default = ''
    )

    # Color
    color = models.CharField (
        verbose_name = 'Color', 
        max_length = 100,
        default = ''
    )

    # Imágen portada
    imagen = models.ImageField (
        verbose_name = 'Imagen',
        upload_to = "coches/",
        blank=True,
        null=True
    )

    # Fecha de la última modificación
    fecha_modificacion = models.DateField (
        auto_now = True
    )

    creado_por = models.ForeignKey(
        Employee, 
        verbose_name = 'Creado por', 
        on_delete = models.CASCADE
    ) 

    extras = models.ManyToManyField( 
        Extra,
        verbose_name = 'Extras',
        related_name = 'coches', 
        blank=True 
    )


    def __str__(self):
        return self.marca + " " + self.modelo



# El resto de imágenes de los coches
class CarImages(models.Model):

    # Relación con la tabla Cars
    car = models.ForeignKey (
        Cars, 
        on_delete = models.CASCADE, 
        related_name = 'imagenes_adicionales'
    )

    # Imagen adicional
    imagen = models.ImageField(
        verbose_name = 'Imagen Adicional',
        upload_to = "coches/galeria/",
        default = "",
        blank = True,
        null = True
    )

    def __str__(self):
        return f"Imagen de {self.car.marca} {self.car.modelo}"

