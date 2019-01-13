from django.http import HttpResponse
from .models import Movies
from django.db import connections

def root(request):
    root_file = open("../public/index.html")
    response = HttpResponse(root_file.read())
    root_file.close()
    return response

def public(request):
    path = ".."+request.path
    static_file = open(path)
    response = HttpResponse(static_file.read(),content_type='application/javascript')
    static_file.close()
    return response

