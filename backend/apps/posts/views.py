from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User

from .forms import PostForm
from .models import Post, Comment, View, ViewCount

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_page(request, *args, **kwargs):
    return render(request, 'pages/homepage.html',
        {}, status=200)

def write_page(request, *args, **kwargs):
    return render(request, 'pages/write.html', 
        {'form': PostForm(None)}, status=200)

def detail_page(request, slug, *args, **kwargs):
    unmasked_id = int(slug.split('-')[-1])
    post_id = unmasked_id ^ 0xABCDEF

    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(parent_post=post)

    if not request.session.session_key:
        request.session.create()
    counter = ViewCount.objects.get(viewed_post=post_id)
    ip = request.META['REMOTE_ADDR']
    session = request.session.session_key
    user = None
    if request.user.is_authenticated:
        user = request.user
    
    if not View.objects.filter(
        ip = ip,
        session = session
    ):
        View.objects.create(
            ip = ip,
            session = session,
            user = user,
            counter = counter
        )
    
    return render(request, 'pages/detail.html', 
        {'post': post, 'comments': comments}, status=200)
