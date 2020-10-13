from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('post/<int:post_id>', views.show_post, name='show_post'),
    path('posts/', views.post_list_view, name='all_posts'),
    path('write/', views.post_create_view, name='write')
]