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
        {}, status=200)

def detail_page(request, slug, *args, **kwargs):
    unmasked_id = int(slug.split('-')[-1])
    post_id = unmasked_id ^ 0xABCDEF
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(parent_post=post)
    
    return render(request, 'pages/detail.html', 
        {'post': post, 'comments': comments}, status=200)
