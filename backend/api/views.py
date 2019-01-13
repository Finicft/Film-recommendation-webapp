from django.http import HttpResponse
from .models import Movies
from django.db import connections
import json

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

def node(request):
    imdb_id = request.GET.get('imdb_id')
    movie = Movies.objects.get(imdb_id = imdb_id)
    #jmovie = json.dumps(movie.__dict__)
    jmovie = movie.to_json()
    response = HttpResponse(jmovie,content_type='application/json')
    return response

def children_nodes(request):
    imdb_id = request.GET.get('imdb_id')
    movie = Movies.objects.get(imdb_id = imdb_id)
    #get same genres 
    list_of_movies = [] 
    same_genres = movie.get_same_genres()
    for key in same_genres:
        for each_movie in same_genres[key]:
            json_movie = each_movie.to_json()
            list_of_movies.append(json_movie + ",")
    
    same_directors = movie.get_same_directors()
    for key in same_directors:
        for each_movie in same_directors[key]:
            json_movie = each_movie.to_json()
            list_of_movies.append(json_movie + ",")

    same_actors = movie.get_same_actors()
    for key in same_actors:
        for each_movie in same_actors[key]:
            json_movie = each_movie.to_json()
            list_of_movies.append(json_movie + ",")

    response = HttpResponse(list_of_movies,content_type='application/json')
    return response