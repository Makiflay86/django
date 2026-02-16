"""
URL configuration for agencia_coches project.

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

# Activamos el soporte de imágenes
from django.conf import settings 
from django.conf.urls.static import static

from app_agencia_coches import views # Importamos todas las vistas de nuestra app


urlpatterns = [
    path('admin/', admin.site.urls),

    path('hola_mundo/', views.hola_mundo),
    path('home/', views.home, name='home'),
    path('cars/', views.cars, name='cars'),
    path('cars_create/', views.cars_create, name='cars_create'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
]


if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)