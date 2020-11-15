from django.urls import path, include
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('write/', views.write_page, name='write_page'),
    path('post/<str:slug>/', views.detail_page, name='detail_page')
]