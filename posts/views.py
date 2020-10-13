from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Post
# Create your views here.

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
    