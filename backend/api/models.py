from django.db import models


class Movies(models.Model):
    imdb_index = models.TextField(blank=True, null=True)
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