from django.conf import settings

from rest_framework import serializers

from .models import Post, Comment, View

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

class ListedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'author_name',
            'title', 
            'summary',
            'comment_count', 
            'timestamp',
            'slug'
        ]

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'author_name',
            'title',
            'summary',
            'html_content',
            'comment_count',
            'timestamp'
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
        if data['author_name'] is None:
            data['author_name'] = 'anonymous'
        return data


class CommentSerializer(serializers.ModelSerializer):
    # add a SerializerMethodField for number of children comments
    class Meta:
        model = Comment
        fields = [
            'id', 
            'author_name',
            'parent', 
            'comment', 
            'timestamp',
            'tree_id'
        ]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'author_name',
            'parent_post',
            'parent',
            'comment'
        ]

    def validate_data(self, data):
        if len(data['comment']) == 0:
            raise serializers.ValidationError(f"Comment cannot be empty.")
        return data

    # this is called when you save the serializer (serializer.save)
    def create(self, validated_data):
        parent_post = validated_data.get('parent_post')
        parent_post.comment_count += 1
        parent_post.save()
        return Comment.objects.create(**validated_data)
