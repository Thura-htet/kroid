from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('write/', views.write_page, name='write_page'),
    path('api/', include([
        path('posts/', views.post_list_view, name='all_posts'),
        path('post/<str:slug>/', views.post_detail, name='post_detial'),
        path('post/<str:slug>/comments/', views.comment, name='comments')
    ]))
]