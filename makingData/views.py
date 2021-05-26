from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model
from movies.models import Movie, Genre
from movies.serializers import GenreSerializer
from community.models import Review

import requests
import logging, traceback
import datetime
from django_seed import Seed

# Create your views here.

# 장르 데이터베이스에 넣기
@api_view(['GET'])
def genre_data(request) :
    res = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=669e119f2e7f069615e4be9aa1ced416&language=ko")
    data = res.json()["genres"]
    serializer = GenreSerializer(data=data, many=True)

    try :
        serializer.is_valid(raise_exception=True)
    except :
        logging.error(traceback.format_exc())
    
    if serializer.is_valid() :
        serializer.save()
    return Response(serializer.data)


# 영화 데이터 데이터베이스에 넣기 
@api_view(['GET'])
def movie_data2(request) :
    link = "http://api.themoviedb.org/3/movie/popular?api_key=669e119f2e7f069615e4be9aa1ced416&language=ko&page="
    
    for tmp in Movie.objects.all() :
        tmp.delete()

    for page in range(1,501) :
        res = requests.get(link+str(page))
        data_list = res.json()["results"]

        for movie_data in data_list :
            movie_id = movie_data["id"]
            link_detail = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=57644a3982e36f38719f5d7cbed9b2ad&append_to_response=videos&language=ko"
            res2 = requests.get(link_detail)
            data = res2.json()

            title = data.get('title')
            

            vote_count = int(data.get("vote_count"))
            vote_average = float(data.get("vote_average"))
            overview = data.get("overview")
            poster_path = data.get("poster_path")
            try :
                video_path = data.get("videos").get("results")[0].get("key")
                release_date = datetime.datetime.strptime(data.get("release_date"), '%Y-%m-%d')
                if not release_date :
                    continue
            except :
                continue

            movie = Movie.objects.create(id = movie_id, 
                title = title,
                release_date= release_date,
                vote_count=vote_count,
                vote_average=vote_average,
                overview=overview,
                poster_path=poster_path,
                video_path=video_path,
            )
            for movie_genre in data.get('genres') :
                genre = Genre.objects.get(pk=movie_genre.get("id"))
                movie.genres.add(genre)

    return Response()

# user, community 에 더미 데이터 넣기
@api_view(['GET'])
def dummyData(request) :
    seeder = Seed.seeder(locale)

    seeder.add_entity(get_user_model(), 50)
    seeder.add_entity(Review, 100)

    inserted_pks= seeder.execute()
    return Response(inserted_pks)




