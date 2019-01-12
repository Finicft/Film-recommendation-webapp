import os
import re
import requests
import time
import traceback
from pyquery import PyQuery as pq

def flush(file):
    file.flush()
    os.fsync(file.fileno())

def main():
    page = 0
    index = 1
    base_url = "https://www.imdb.com"
    next_url = "/search/title?release_date=1900-01-01,2019-01-31&count=250&ref_=adv_nxt"
    take = 250
    output_file = open("data.csv","a")
    log_file = open("log.txt","w")

    while(True):
        try:
            # querystring = {"release_date":"1950-01-01,2019-01-31","languages":"en","count":str(take),"start":str(page*take+1),"ref_":"adv_nxt"}

            response = requests.request("GET", base_url+next_url)
            root = pq(response.text)
            movie_divs = root('.lister-item.mode-advanced')
            for movie_div in movie_divs:
                try:
                    movie_div_root = root(movie_div)
                    image_url = movie_div_root('.lister-item-image.float-left a img.loadlate').attr('loadlate').replace('@._V1_UX67_CR0,0,67,98_AL_.jpg','@._V1_SY1000_CR0,0,674,1000_AL_.jpg')
                    imdb_id = movie_div_root('.lister-item-image.float-left a img.loadlate').attr('data-tconst')

                    main_data_div = movie_div_root('.lister-item-content')

                    title = main_data_div('.lister-item-header a').text()
                    year = re.sub(r"[() ]", '', main_data_div('.lister-item-header .lister-item-year').text())

                    content_rating = main_data_div('p.text-muted span.certificate').text()
                    genres = main_data_div('.text-muted span.genre').text().split(',')

                    map(str.strip, genres)

                    genre_1 = ''
                    genre_2 = ''
                    genre_3 = ''
                    if len(genres)>0:
                        genre_1 = genres[0]
                        if len(genres)>1:
                            genre_2 = genres[1]
                            if len(genres)>2:
                                genre_3 = genres[2]

                    runtime = ''
                    runtime_span_parts = main_data_div('.text-muted span.runtime').text().split()
                    if len(runtime_span_parts) > 0:
                        runtime = runtime_span_parts[0]

                    imdb_rating = main_data_div('.ratings-bar .inline-block.ratings-imdb-rating strong').text()

                    creators_div = root(main_data_div('p')[2])
                    directors_elements = creators_div('a[href*="_dr_"]')
                    actors_elements = creators_div('a[href*="_st_"]')

                    directors = []
                    for directors_element in directors_elements:
                        directors.append(root(directors_element).text())

                    director_1=''
                    director_2=''
                    director_3=''

                    if len(directors) > 0:
                        director_1=directors[0]
                        if len(directors) > 1:
                            director_2=directors[1]
                            if len(directors) > 2:
                                    director_3=directors[2]

                    actors = []
                    for actors_element in actors_elements:
                        actors.append(root(actors_element).text())

                    actor_1=''
                    actor_2=''
                    actor_3=''

                    if len(actors) > 0:
                        actor_1 = actors[0]
                        if len(actors) > 1:
                            actor_2 = actors[1]
                            if len(actors) > 2:
                                actor_3 = actors[2]
                    
                    other_stats_elements = main_data_div('.sort-num_votes-visible span[name="nv"]')
                    imdb_votes = ''
                    
                    gross = ''
                    if len(other_stats_elements)>0:
                        imdb_votes = root(other_stats_elements[0]).attr('data-value')
                    if len(other_stats_elements)==2:
                        gross = root(other_stats_elements[1]).attr('data-value').replace(',','')

                    output_file.write("\""+"\",\"".join([str(index),imdb_id,title,year,content_rating,":".join(genres),":".join(directors),":".join(actors),str(runtime),imdb_rating,imdb_votes,gross,director_1,director_2,director_3,actor_1,actor_2,actor_3,genre_1,genre_2,genre_3,image_url])+"\"")
                    output_file.write("\n")
                    flush(output_file)
                except:
                    log_file.write("Problem with: %s at index: %d\n"%(title,index))
                    log_file.write(traceback.format_exc())
                    log_file.write("\n")
                    flush(log_file)
                    traceback.print_exc()
                index += 1
            time.sleep(5)
            page+=1
            next_url = root('.desc a[href$="ref_=adv_nxt"]').attr('href')
            print("Page %d successful"%page)
            # if(page == 2):
            #     break

        except:
            log_file.write(traceback.format_exc())
            log_file.write("\n")
            flush(log_file)
            traceback.print_exc()


if __name__ == "__main__":
    main()