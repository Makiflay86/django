from django.shortcuts import render
from django.http import HttpResponse

def hola_mundo (request):
    return HttpResponse ("<h1>hola mundo</h1>")

def home (request):
    return render(request,'index.html')