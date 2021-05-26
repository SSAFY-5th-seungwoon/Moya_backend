from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework import generics

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Movie, Genre, Tournament
from .serializers import MovieSerializer, GenreSerializer, TournamentSerializer, MovieDetailSerializer

from community.models import Review
from community.serializers import ReviewListSerializer

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
    # serializer = MovieDetailSerializer(data = movie)
    serializer = MovieDetailSerializer(data = movie_list, many=True)

    # 한영화의 genres에 포함된 genre를 포함하는 genres를 가지고 있는 영화들을 찾고 싶다. - 해결
    
    genres = movie.genres.all().values_list('id', flat=True) # 영화의 모든 genre를 id 객체로 가져오기
    movies_same_genre = Movie.objects.filter(genres__id__in=genres).order_by('-vote_count').distinct()[:20]

    # recommended_movies = Movie.objects.filter(genres = movie.genres.all())[:10]
    same_genre_serializer = MovieDetailSerializer(data = movies_same_genre, many=True)
    print(serializer.is_valid(), same_genre_serializer.is_valid())
    context = {
        "movie" : serializer.data, 
        "same_genres" : same_genre_serializer.data,
    }

    # movieSerializer = MovieSerializer(data = recommended_movies, many=True)
    return Response(context)

@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def tournament(request) :
    if request.method == 'GET' :
        random_movies = Movie.objects.order_by('?')[:16]
        serializer = MovieSerializer(data = random_movies, many=True)
        print(serializer.is_valid())
        return Response(serializer.data)
    elif request.method =='POST' : 
        # 작업중
        movie_id = request.data["movie_id"]
        user = request.user
        print(user)
        movie = Movie.objects.get(pk=movie_id)
        tournament = Tournament.objects.create(
            movie = movie, 
            user = request.user
        )

        serializer = TournamentSerializer(data= tournament)
        print(serializer.is_valid())
        return Response(serializer.data)

@api_view(['GET'])
def mypageMovie(request, username) :
    person = get_object_or_404(get_user_model(), username=username)
    winMovies = Movie.objects.filter(tournament__user=person) # OneToMany 접근
    likeMovies = Review.objects.filter(user=person).filter(liked=True).order_by('-created_at')

    winMoviesSerializer = MovieSerializer(data = winMovies, many=True)
    likeMoviesSerializer = ReviewListSerializer(data= likeMovies, many=True)

    print(winMoviesSerializer.is_valid(), likeMoviesSerializer.is_valid())
    context = {
        'winMovies' : winMoviesSerializer.data, 
        'likeMovies' : likeMoviesSerializer.data
    }
    return Response(context)





