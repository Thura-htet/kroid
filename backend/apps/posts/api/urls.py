from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^posts/(?P<username>\w+|)/?$',
        views.post_list_view,
        name='all_posts'),
    path('post/<str:slug>/', views.post_detail, name='post_detial'),
    path('post/<str:slug>/comments/', views.comment, name='comments')
]