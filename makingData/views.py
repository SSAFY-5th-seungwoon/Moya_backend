from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model
from movies.models import Movie, Genre, Tournament
from movies.serializers import GenreSerializer
from community.models import Review, Comment

import requests
import logging, traceback
import datetime
import random
from faker import Faker
from django_seed import Seed
from django.http.response import JsonResponse
# Create your views here.

@api_view(['GET'])
def wakeUp(request) :
    return JsonResponse({'message' : '켜져욧'})

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
    fake = Faker()
    seeder = Seed.seeder('ko_KR')

    print(fake.name())
    print(fake.email())
    print(seeder.faker.password())
    for i in range(100) :
        get_user_model().objects.create(
            username = fake.name(),
            email =fake.email(),
            password =seeder.faker.password(),
        )
    print("체크1")


    movie_all = Movie.objects.all().order_by("?")[:10]
    user_all = get_user_model().objects.all()[:100]


    print(random.choice(movie_all))
    print(random.choice(user_all))
    for i in range(100) :
        Review.objects.create(
            title =f'{i}번째 글제목',
            liked = True,
            content= f'{i}번째 글의 글내용',
            movie= random.choice(movie_all),
            user= user_all[i]
        )
    
    print("실행2")

    reviews = Review.objects.all()

    for i in range(300) :
        Comment.objects.create(
            user = random.choice(user_all),
            review = random.choice(reviews),
            content = f"{i}번째 댓글내용"
        )

    return Response("됩니다")




