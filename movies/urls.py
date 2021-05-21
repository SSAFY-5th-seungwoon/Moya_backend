from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:movie_pk>/', views.detail, name='detail'),
    # path('tournament', views.tournament, name='tournament'),
    path('', views.main),
    path('<movie_pk>/detail', views.movie_detail),
    path('genre_data', views.genre_data),
    path('movie_data2', views.movie_data2)

]
