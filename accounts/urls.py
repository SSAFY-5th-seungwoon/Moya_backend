from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', obtain_jwt_token, name='login'), # login jwt 토큰 발급
    path('follow/<int:user_pk>/', views.follow, name='follow'),
    # path('<int:user_id>/', views.profile, name='profile'),
    path('<str:username>/', views.profile, name='profile'),
]
