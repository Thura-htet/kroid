from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer, PostActionSerializer
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
        return Response(serializer.data)

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
    serializer = PostActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get('id')
        action = data.get('action')
        qs = Post.objects.get(id=post_id)
        if not qs.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj = qs.first()
        serializer = PostSerializer(obj)
        user = request.user
        if action == 'unlike':
            obj.likes.remove(user)
        elif action == 'like': 
            obj.likes.add(user)
    return Response(serializer.data, status=status.HTTP_200_OK)