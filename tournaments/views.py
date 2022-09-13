from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(response):
    return render(response, 'tournaments/index.html', {})

def test(response):
    return HttpResponse("<h1>Hello test!</h1>")
