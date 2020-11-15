from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.post_list_view, name='all_posts'),
    path('post/<str:slug>/', views.post_detail, name='post_detial'),
    path('post/<str:slug>/comments/', views.comment, name='comments')
]