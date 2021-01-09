from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.profile_view, name="profile_view"),
    path('<str:username>/follow/', views.user_follow_view, name="follow_user")
]