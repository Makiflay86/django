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
from django.urls import path, include

# Activamos el soporte de imágenes
from django.conf import settings 
from django.conf.urls.static import static

from app_agencia_coches import views # Importamos todas las vistas de nuestra app


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.dashboard, name='dashboard'),

    path('cars/', views.cars, name='cars'),
    path('cars_create/', views.cars_create, name='cars_create'),
    path('cars_edit/<int:pk>/', views.cars_edit, name='cars_edit'),
    path('cars_delete/<int:pk>/', views.cars_delete, name='cars_delete'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),

    path('employees/', views.employees, name='employees'),
    path('employees_create/', views.employees_create, name='employees_create'),
    path('employee_edit/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employee_delete/<int:pk>/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),

    path('extras/', views.extras, name='extras'),
    path('extras_create/', views.extras_create, name='extras_create'),
    path('extras_edit/<int:pk>/', views.extras_edit, name='extras_edit'),
    path('extras_delete/<int:pk>/', views.extras_delete, name='extras_delete'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]


if settings.DEBUG: urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)