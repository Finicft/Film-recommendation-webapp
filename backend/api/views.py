from django.http import HttpResponse
from .models import Movies
from django.db import connections

def hello(request):
    movie = Movies.objects.all()
   
   
    return HttpResponse("<p>Hello, world</p>")