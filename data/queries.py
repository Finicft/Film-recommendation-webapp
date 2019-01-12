
#some code from https://github.com/Finicft/291-Mini-project-2-/blob/master/main.py

import sqlite3
import string
import os

connection = None
cursor = None

def connect():

    # connect to .db

    global connection, cursor

    #200,000 entries
    path="./movies.db"

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    

    connection.commit()

    return



def get_all_info(title):
  global connection, cursor
  connect()
  title = string.capwords(title)
  cursor.execute("SELECT imdb_index,imdb_id,title,genres,directors, actors,imdb_rating,image_url  FROM movies WHERE title=:title", {"title":title})
  info = cursor.fetchone()
  info_list = []
  #if movie doesnt exist in the data base
  if type(info) == None:
    print("This movie is not available in the database :( try another movie! ")
    return 0 
  for item in info:
    info_list.append(item)

  return info_list

def get_same_genre(genre):
  global connection, cursor
  connect()

  genre =  "%" + genre + "%"
  genre = '"{}"'.format(genre)
  cursor.execute("SELECT title,imdb_index,imdb_id,imdb_rating,image_url  FROM movies WHERE genres LIKE " + genre  + " ORDER BY random() LIMIT 5")
  movies = cursor.fetchall()
  movie_list = [] 
  #put information in list so they're not sqlite.row objects 
  for movie in movies:
    movie_details = [] 
    for detail in movie:
      movie_details.append(detail)
    movie_list.append(movie_details)
  return movie_list


def get_same_director(director):
  global connection, cursor
  connect()

  director =  "%" + director + "%"
  director = '"{}"'.format(director)

  cursor.execute("SELECT title,imdb_index,imdb_id,imdb_rating,image_url  FROM movies WHERE directors LIKE " + director  + " ORDER BY random() LIMIT 5")
  movies = cursor.fetchall()
  movie_list = [] 

  for movie in movies:
    movie_details = [] 
    for detail in movie:
      movie_details.append(detail)
    movie_list.append(movie_details)

  return movie_list


def get_same_actor(actor):
  global connection, cursor
  connect()

  actor =  "%" + actor + "%"
  actor = '"{}"'.format(actor)

  cursor.execute("SELECT title,imdb_index,imdb_id,imdb_rating,image_url  FROM movies WHERE actors LIKE " + actor  + " ORDER BY random() LIMIT 5")
  movies = cursor.fetchall()
  movie_list = [] 

  for movie in movies:
    movie_details = [] 
    for detail in movie:
      movie_details.append(detail)
    movie_list.append(movie_details)

  return movie_list






