from rest_framework import serializers

from .models import Genre
from .models import Movie
from .models import Tournament

class GenreSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Genre
        fields = "__all__"

class GenreSerializerId(serializers.ModelSerializer): # 데이터 넣을 때

    class Meta : 
        model = Genre
        fields = ('id', )



class MovieSerializer(serializers.ModelSerializer): # 데이터 넣을 때
   
    class Meta : 
        model = Movie
        fields="__all__"

class MovieDetailSerializer(serializers.ModelSerializer): # 일단 만들어 둠
    genres = GenreSerializerId(many=True)

    class Meta : 
        model = Movie
        exclude = ('video_path', )

class TournamentSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = Tournament
        fields = "__all__"
