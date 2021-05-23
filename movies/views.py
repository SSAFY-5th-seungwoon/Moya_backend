from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# from rest_framework import generics

from django.shortcuts import get_object_or_404
from .models import Movie, Genre, Tournament
from .serializers import MovieSerializer, GenreSerializer, TournamentSerializer, MovieDetailSerializer

from rest_framework.views import APIView
from django.http import Http404
import requests
import logging, traceback
import datetime

from django.http.response import JsonResponse

@api_view(['GET'])
def main(request) :
    latest_movies = Movie.objects.order_by('-release_date')[:20]
    highscore_movies = Movie.objects.order_by('-vote_average')[:20]
    like_movies = Movie.objects.order_by('-vote_count')[:20]

    latest_serializer = MovieSerializer(data=latest_movies, many=True)
    highscore_serializer = MovieSerializer(data=highscore_movies, many=True)
    like_serializer = MovieSerializer(data=like_movies, many=True)

    print(latest_serializer.is_valid() , highscore_serializer.is_valid() , like_serializer.is_valid())
    
    context={
        'latest_movies' : latest_serializer.data,
        'highscore_movies' : highscore_serializer.data,
        'like_movies' : like_serializer.data,
    }
    return JsonResponse(context)


@api_view(['GET'])
def movie_detail(request, movie_pk) :
    movie = Movie.objects.get(pk=movie_pk)
    movie_list = [movie]

    serializer = MovieDetailSerializer(data = movie_list, many=True)
    # 한영화의 genres에 포함된 genre를 포함하는 genres를 가지고 있는 영화들을 찾고 싶다. - 해결못함
    '''
    SELECT * 
    FROM moives
    WHERE genres in (SELECT genres FROM movies where id = movie_pk)
    '''

    # recommended_movies = Movie.objects.filter(genres = movie.genres.all())[:10]

    print(serializer.is_valid())

    # movieSerializer = MovieSerializer(data = recommended_movies, many=True)
    return Response(serializer.data)



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