from rest_framework import serializers
from .models import Post, Comment, User

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author_name', 'parent', 'level']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    # We send comments as a FLAT list. 
    # It is faster to send 100 flat items and let JS build the tree 
    # than to do recursive serialization in Python.
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'author_name', 'comments']

class UserSerializer(serializers.ModelSerializer):
    total_karma = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'total_karma']