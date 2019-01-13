from django.db import models
from django.db import connections
import json
import random


class Movies(models.Model):
    imdb_index = models.TextField(blank=True,primary_key=True)
    imdb_id = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    content_rating = models.TextField(blank=True, null=True)
    genres = models.TextField(blank=True, null=True)
    directors = models.TextField(blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    runtime = models.TextField(blank=True, null=True)
    imdb_rating = models.TextField(blank=True, null=True)
    imdb_votes = models.TextField(blank=True, null=True)
    gross = models.TextField(blank=True, null=True)
    director_1 = models.TextField(blank=True, null=True)
    director_2 = models.TextField(blank=True, null=True)
    director_3 = models.TextField(blank=True, null=True)
    actor_1 = models.TextField(blank=True, null=True)
    actor_2 = models.TextField(blank=True, null=True)
    actor_3 = models.TextField(blank=True, null=True)
    genre_1 = models.TextField(blank=True, null=True)
    genre_2 = models.TextField(blank=True, null=True)
    genre_3 = models.TextField(blank=True, null=True)
    image_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'

    def get_title(self):
        return self.title

    def get_imdb_index(self):
        return self.imdb_index

    def get_imdb_id(self):
        return self.imdb_id
    
    def get_image_url(self):
        return self.image_url
    
    def get_imdb_rating(self):
        return self.imdb_rating

    def get_same_genres(self):
        movie_genres = [] 
        same_genre_movies = [] 
        if self.genre_1 is not "":
            movie_genres.append(self.genre_1)
            genre1_movies = Movies.objects.filter(genres__contains = self.genre_1)
            random_genre_1_movies = random.sample(list(genre1_movies),3)
            same_genre_movies.append(random_genre_1_movies)
        if self.genre_2 is not "":
            movie_genres.append(self.genre_2)
            genre2_movies = Movies.objects.filter(genres__contains = self.genre_2)
            random_genre_2_movies = random.sample(list(genre2_movies),3)
            same_genre_movies.append(random_genre_2_movies)
     
        if self.genre_3 is not "":
            movie_genres.append(self.genre_3)
            genre3_movies = Movies.objects.filter(genres__contains = self.genre_3)
            random_genre_3_movies = random.sample(list(genre3_movies),3)
            same_genre_movies.append(random_genre_3_movies)
    
        movies = dict(zip(movie_genres, same_genre_movies))
        return movies
    
    def get_same_actors(self):
        film_actors = [] 
        same_actors_films = [] 
        if self.actor_1 is not "":
            film_actors.append(self.actor_1)
            actor_1_movies = Movies.objects.filter(actors__contains = self.actor_1)
            random_actor_1_movies = random.sample(list(actor_1_movies),3)
            same_actors_films.append(random_actor_1_movies)
        if self.actor_2 is not "":
            film_actors.append(self.actor_2)
            actor_2_movies = Movies.objects.filter(actors__contains = self.actor_2)
            random_actor_2_movies = random.sample(list(actor_2_movies),3)
            same_actors_films.append(random_actor_2_movies)
        if self.actor_3 is not "":
            film_actors.append(self.actor_3)
            actor_3_movies = Movies.objects.filter(actors__contains = self.actor_3)[:3]
            random_actor_3_movies = random.sample(list(actor_3_movies),3)
            same_actors_films.append(random_actor_3_movies)
        
        movies = dict(zip(film_actors,same_actors_films))
        return movies

    def get_same_directors(self):
        film_directors = [] 
        same_director_films = [] 
        if self.director_1 is not "":
            film_directors.append(self.director_1)
            director_1_movies = Movies.objects.filter(directors__contains = self.director_1)
            random_director_1_movies = random.sample(list(director_1_movies),3)
            same_genre_movies.append(random_director_1_movies)
        if self.director_2 is not "":
            film_directors.append(self.director_2)
            director_2_movies = Movies.objects.filter(directors__contains = self.director_2)
            random_director_2_movies = random.sample(list(director_2_movies),3)
            same_genre_movies.append(random_director_2_movies)
        if self.director_3 is not "":
            film_directors.append(self.director_3)
            director_3_movies = Movies.objects.filter(directors__contains = self.director_3)
            random_director_3_movies = random.sample(list(director_3_movies),3)
            same_genre_movies.append(random_director_3_movies)
        movies = dict(zip(film_directors,same_director_films))
        return movies

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
  