import json
import re
import requests
import random
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
            if each_movie != movie:
                json_movie = each_movie.to_json()
                list_of_movies.append(json_movie + ",")
    
    same_directors = movie.get_same_directors()
    for key in same_directors:
        for each_movie in same_directors[key]:
            if each_movie != movie:
                json_movie = each_movie.to_json()
                list_of_movies.append(json_movie + ",")
    

    same_actors = movie.get_same_actors()
    for key in same_actors:
        for each_movie in same_actors[key]:
            if each_movie != movie:
                json_movie = each_movie.to_json()
                list_of_movies.append(json_movie + ",")
    
    string_movies = ''.join(random.sample(list_of_movies,min(len(list_of_movies),5)))
    string_movies = string_movies[:-1]
    string_movies = "[" + string_movies + "]"

    response = HttpResponse(string_movies,content_type='application/json')
    return response
    
def search(request):
    phrase = request.GET['phrase']
    url =('https://v2.sg.media-imdb.com/suggests/%s/%s.json'%(phrase[0].lower(),phrase.lower())).replace(' ','_')
    data_response = requests.get(url)
    data = re.sub(r"^imdb\$\w+\(","[",data_response.text)
    data = re.sub(r"}\)$","}]",data)
    data_json = json.loads(data)[0]["d"]
    result_array=[]
    for item in data_json:
        if(re.match(r"tt\d+",item["id"])):
            result_array.append({
                "name": item["l"],
                "id": item["id"],
                "year": item["y"]
            })
    response = HttpResponse(json.dumps(result_array),content_type='application/json')
    return response
