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
    genres = GenreSerializerId(many=True, read_only=True)

    class Meta : 
        model = Movie
        fields = '__all__'



class MovieDetailSerializer(serializers.ModelSerializer): # 일단 만들어 둠
    
    class Meta : 
        model = Movie
        fields = "__all__"
        read_only_fields = ('genre',)

class TournamentSerializer(serializers.ModelSerializer): 
    class Meta : 
        model = Tournament
        fields = "__all__"
