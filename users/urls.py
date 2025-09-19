# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.profile, name='profile'),

    # 🔹 Balans artırma səhifəsi
    path('balans-artir/', views.balans_artir, name='balans_artir'),
]
