from rest_framework import serializers

from .models import Review
from .models import Comment

class ReviewSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Review
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Comment
        fields = "__all__"