from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('write/', views.write_page, name='write'),
    path('posts/', views.post_list_view, name='all_posts'),
    path('post/<int:post_id>', views.post_detail, name='post_detial'),
    path('post/<int:post_id>/comments', views.comment, name='comments')
]