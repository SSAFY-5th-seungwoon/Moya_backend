from rest_framework.response import Response
from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework import generics

from django.shortcuts import get_object_or_404
from .models import Movie, Genre, Tournament
from .serializers import MovieSerializer, GenreSerializer, TournamentSerializer

from rest_framework.views import APIView
from django.http import Http404
import requests
import logging, traceback


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


# 영화 데이터 데이터베이스에 넣기 - 포기
@api_view(['GET'])
def genre_data(request) :
    link = "http://api.themoviedb.org/3/movie/popular?api_key=669e119f2e7f069615e4be9aa1ced416&language=ko&page="
    
    
    for page in range(1,2) :
        res = requests.get(link+str(page))
        data_list = res.json()["results"]

        for movie in data_list :
            movie_id = movie["id"]
            link_detail = "https://api.themoviedb.org/3/movie/{movie_id}?api_key=57644a3982e36f38719f5d7cbed9b2ad&append_to_response=videos&language=ko"
            res2 = requests.get(link_detail)
            data = res2.json()
            serializer = MovieSerializer(data=data, many=True)

            try :
                serializer.is_valid(raise_exception=True)
            except :
                logging.error(traceback.format_exc())
            
            if serializer.is_valid() :
                serializer.save()
    return Response(serializer.data)
