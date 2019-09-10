from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'basic/index.html')

def about(request):
    return render(request, 'basic/about.html')