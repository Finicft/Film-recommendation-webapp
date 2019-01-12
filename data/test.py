from queries import get_all_info,get_same_genre, get_same_director, get_same_actor

def main():
	movie_title = input("enter the name of the title: ")
	info = get_all_info(movie_title)
	print(info)
	#if movie exists in database
	if info != 0:
		genres = info[3].split(":")
		directors = info[4].split(":")
		actors = info[5].split(":")
		#put movies in dictionary of genres
		genre_movies = [] 
		for genre in genres:
			movies = get_same_genre(genre)
			genre_movies.append(movies)
		genre_dict = dict(zip(genres, genre_movies))
		print(genre_dict)

		director_movies = [] 
		for director in directors:
			movies = get_same_director(director)
			director_movies.append(movies)
		director_dict = dict(zip(directors, director_movies))
		print(director_dict)

		actors_movies = [] 
		for actor in actors:
			movies = get_same_actor(actor)
			actors_movies.append(movies)
		actors_dict = dict(zip(actors, actors_movies))
		print(actors_dict)







main()