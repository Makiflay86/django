"""
URL configuration for ProyectoBase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from HolaMundo import views # Importo nuestro módulo views, recién creado.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hola/', views.hola_mundo), # Si queremos que se habra por defecto debemos de no ponerle un nombre en las 
                                     # comimllas "path('', views.hola_mundo)"
    path('index/', views.home),
    path('author/', views.author),
    path('book/', views.book)
]
