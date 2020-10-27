from rest_framework import serializers

from django.conf import settings
from .models import Post, Comment

MAX_TITLE_LENGTH = settings.MAX_TITLE_LENGTH
MAX_SUMMARY_LENGTH = settings.MAX_SUMMARY_LENGTH
POST_ACTION_OPTIONS = settings.POST_ACTION_OPTIONS


class PostActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, action):
        action = action.lower().strip()
        if not action in POST_ACTION_OPTIONS:
            raise serializers.ValidationError('This is not a valid action for this tweet')
        return action

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'author',
            'title', 
            'summary', 
            'content', 
            'view_count', 
            'argument_count', 
            'timestamp',
            'slug'
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'content']
    
    def validate_data(self, data):
        if len(data['title']) > MAX_TITLE_LENGTH:
            raise serializers.ValidationError(f"The title must not be more than {MAX_TITLE_LENGTH} characters long.")
        if len(data['summary']) > MAX_SUMMARY_LENGTH:
            raise serializers.ValidationError(f"The summary must not be more than {MAX_SUMMARY_LENGTH} characters long.")
        if len(data['content']) == 0:
            raise serializers.ValidationError(f"Content cannnot be empty.")
        if data['author'] is None:
            data['author'] = 'anonymous'
        return data


# really need to review this Serializer
class CommentSerializer(serializers.ModelSerializer):
    # add a SerializerMethodField for number of comments
    class Meta:
        model = Comment
        fields = [
            'author', 
            'parent_post', 
            'parent', 
            'comment', 
            'timestamp'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment']

    def validate_data(self, data):
        if len(data['comment']) == 0:
            raise serializers.ValidationError(f"Comment cannot be empty.")
        return data