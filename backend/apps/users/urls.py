from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
    path('register/', views.resgister_view, name='register_page')
]