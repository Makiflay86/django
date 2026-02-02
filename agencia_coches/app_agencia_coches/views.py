from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def hola_mundo (request):
    return HttpResponse ("<h1>hola mundo</h1>")

def home (request):
    cars = Cars.objects.all()
    return render(request,'index.html',{'cars':cars})
