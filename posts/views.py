from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer
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


# ==========
# OLD ROUTES
# ==========
# def post_list_view(request, *args, **kwargs):
#     try:
#         status = 200
#         qs = Post.objects.all()
#         posts_list = [x.serialize() for x in qs]
#         data = {
#             'response': posts_list,
#             'message': 'success'
#         }
#     except:
#         data['message'] = 'error: page not found'
#         status = 400
#     return JsonResponse(data, status=status)

# turn this into an API end point and ajax
def post_create_view(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    # also add error handling
    # have to implement safe redirecting
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        url = reverse('posts:home_page')
        if is_safe_url(url, ALLOWED_HOSTS):
            return redirect(url)
    # Bad design here you need to turn this to an api end point
    # And also handle error on JS side after you've implemented it
    # turn form.html to use pure javascript to handle ajax and all that
    if form.errors:
        return JsonResponse(form.errors, status=400)
    return render(request, 'pages/form.html', {'form': form})


def show_post(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(id=post_id)
        data = {
            'response': post.serialize(),
            'message': 'success'
        }
        status = 200
    except:
        data['message'] = 'error: page not found'
        status = 404
    return JsonResponse(data, status=status)