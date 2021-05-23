from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.reviews, name ='reviews'),
    path('<int:movie_id>/review/',views.review_craeted, name='review_craeted'),
    path('<int:review_id>/',views.review_detail, name='review_detail')
] 
