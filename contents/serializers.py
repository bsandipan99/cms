from rest_framework import serializers
from .models import Post

class PostSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Post
        fields = ['title','text','author','created_date','published_date']