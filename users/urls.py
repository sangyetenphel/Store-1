# from django.contrib.auth import views as auth_views
from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user-register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('login', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),
    path('review_delete/<int:id>', views.user_review_delete, name='user-review-delete'),
]
