from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .forms import PostForm
from .models import Post
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_page(request, *args, **kwargs):
    return render(request, 'pages/homepage.html', {}, status=200)

def post_list_view(request, *args, **kwargs):
    try:
        status = 200
        qs = Post.objects.all()
        posts_list = [
            {
                'id': x.id,
                'title': x.title,
                'summary': x.summary,
                'content': x.content
            } for x in qs]
        data = {
            'response': posts_list,
            'message': 'success'
        }
    except:
        data['message'] = 'error: page not found'
        status = 400
    return JsonResponse(data, status=status)

def show_post(request, post_id, *args, **kwargs):
    try:
        post = Post.objects.get(id=post_id)
        data = {
            'response': {
                'id': post.id,
                'title': post.title,
                'summary': post.summary,
                'content': post.content
            },
            'message': 'success'
        }
        status = 200
    except:
        data['message'] = 'error: page not found'
        status = 404
    return JsonResponse(data, status=status)

def post_create_view(request, *args, **kwargs):
    form = PostForm(request.POST or None)
    # have to implement safe redirecting
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        url = reverse('posts:home_page')
        if is_safe_url(url, ALLOWED_HOSTS):
            return redirect(url)
    return render(request, 'pages/form.html', {'form': form})