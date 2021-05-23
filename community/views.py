from django.shortcuts import render

from .models import Review, Comment
from movies.models import Movie
from .serializers import ReviewSerializer,ReviewListSerializer

from django.shortcuts import get_object_or_404,get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http.response import JsonResponse
# Create your views here.
@api_view(['get'])
def reviews(request):
    reviews = Review.objects.all()[:20]
    #review = get_list_or_404(Review)
    #reviewserializer = ReviewListSerializer(review, many=True)    
    reviewserializer = ReviewSerializer(data=reviews, many=True)
    print(reviewserializer.is_valid())
    return Response(reviewserializer.data)
@api_view(['get'])
def review_detail(request,review_id):
    review = get_object_or_404(Review, id=review_id)
    review_list = [review]
    
    reviewserializer = ReviewSerializer(data=review_list, many=True)
    print(reviewserializer.is_valid())
    return Response(reviewserializer.data)

@api_view(['post'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def review_craeted(request,movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    # movie = Movie.objects.filter(id=movie_id)
    print(movie)
    serializer = ReviewSerializer(data =request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user = request.user)
        return Response(serializer.data, status= status.HTTP_201_CREATED)