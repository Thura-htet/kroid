from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .forms import PostForm
from .models import Post, Comment
from .serializers import (
    PostSerializer, 
    PostCreateSerializer,
    PostActionSerializer, 
    CommentSerializer,
    CommentCreateSerializer)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_page(request, *args, **kwargs):
    return render(request, 'pages/homepage.html', {}, status=200)

def write_page(request, *args, **kwargs):
    return render(request, 'pages/write.html', {'form': PostForm(None)}, status=200)

def detail_page(request, slug, *args, **kwargs):
  
    unmasked_id = int(slug.split('-')[-1])
    post_id = unmasked_id ^ 0xABCDEF

    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(parent_post=post)

    return render(request, 'pages/detail.html', {
        'post': post,
        'comments': comments}, status=200)


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def post_list_view(request, *args, **kwargs):

    if request.method == 'GET':
        # show all posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        # create a new post
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # the first save does not have the slug
            post = serializer.save(author=request.user)
            # saving to get the slug (probably not the best practice) 
            # already tried using the receiver but it didn't work
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# will later involve ['PUT'] as well
@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail(request, slug, *args, **kwargs):

    try:
        unmasked_id = int(slug.split('-')[-1])
        post_id = unmasked_id ^ 0xABCDEF
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def comment(request, slug, *args, **kwargs):
    unmasked_id = int(slug.split('-')[-1])
    post_id = unmasked_id ^ 0xABCDEF

    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(parent_post=post_id)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # get these following data some other way
        comment_to = request.data["parentType"]

        if comment_to not in ['comment', 'post']:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            parent_post = Post.objects.get(id=post_id)
            if comment_to == "comment":
                parent_id = request.data["parentId"]
                parent_comment = Comment.objects.get(id=parent_id)
            elif comment_to == "post":
                parent_comment = None

        except (Comment.DoesNotExist, Post.DoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        data = {"comment": request.data["comment"]}
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent_post=parent_post, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
