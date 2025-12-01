from django.db import models

# Create your models here.

# Create your models here.
# Al aplicar esta herencia, Django va a saber que Author es una tabla en la BD
class Author (models.Model):

    name=models.CharField (verbose_name='Nombre', # etiqueta dentro de la tabla
        max_length= 100,
        default=''
    )

    last_name=models.CharField(verbose_name='Apellido',
        max_length=150,
        default=''
    )
    
    age=models.PositiveSmallIntegerField (verbose_name='Edad',
        max_length=3
    )

    mail=models.EmailField(verbose_name='Mail', 
        max_length=150,
        default=''
    )