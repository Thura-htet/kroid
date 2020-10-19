from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .forms import PostForm
from .models import Post, Comment
from .serializers import PostSerializer, PostActionSerializer, CommentSerializer
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_page(request, *args, **kwargs):
    return render(request, 'pages/homepage.html', {}, status=200)

def write_page(request, *args, **kwargs):
    return render(request, 'pages/write.html', {'form': PostForm(None)}, status=200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_view(request, *args, **kwargs):
    if request.method == 'GET':
        # show all posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        # create a new post
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# will later involve ['PUT', 'DELETE'] as well
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# testing purposes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_action(request, *args, **kwargs):
    # serialize the post action first
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get('id')
        action = data.get('action')
        
        # try to get the post by the id of post_id
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # serializer the returned post
        serializer = PostSerializer(post)
        user = request.user
        if action == 'unlike':
            post.likes.remove(user)
        elif action == 'like': 
            post.likes.add(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment(request, post_id, *args, **kwargs):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(post=post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        # there is no data in request.POST 
        # request.POST will only store form data
        # the posted data is in request.data
        parent_type = request.data["parentType"]
        parent_id = request.data["parentId"]

        if (not all([parent_id, parent_type]) or 
            parent_type not in ['comment', 'post']):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            if parent_type == "comment":
                parent = Comment.objects.get(id=parent_id)
            elif parent_type == "post":
                parent = None

        except (Comment.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, parent=parent)
            return Response(serializer.data, status=status.HTTP_200_OK)
