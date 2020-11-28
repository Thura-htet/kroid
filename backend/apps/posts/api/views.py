from ipware import get_client_ip

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..forms import PostForm
from ..models import Post, Comment, View, ViewCount

from ..serializers import (
    PostSerializer,
    ListedPostSerializer, 
    PostCreateSerializer,
    PostActionSerializer, 
    CommentSerializer,
    CommentCreateSerializer)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_view(request, username, *args, **kwargs):
    if request.method == 'GET':
        if username:
            posts = Post.objects.filter(author__username=username)
        else:
            posts = Post.objects.all()
        serializer = ListedPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    else:
        serializer = PostCreateSerializer(data=request.data) # an instance of post to be created
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(username=request.user)
            serializer.save(author=request.user, author_name=user.username)
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
        if not request.session.session_key:
            request.session.create()
        counter = ViewCount.objects.get(viewed_post=post_id)
        ip, is_routable = get_client_ip(request)
        session = request.session.session_key
        user = None
        if request.user.is_authenticated:
            user = request.user
        # maybe i should filter on just the ip?
        if not View.objects.filter(ip = ip, session = session):
            View.objects.create(
                ip = ip,
                session = session,
                user = user,
                counter = counter
            )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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

        data = {
            "comment": request.data["comment"]
        }
        serializer = CommentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user, parent_post=parent_post, parent=parent_comment)
            return Response(serializer.data, status=status.HTTP_200_OK)
