from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from stats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('registration/login/', views.login_user, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.logout_user, name="logout"),
    path("name/<name>", views.name, name="name"),
    path('about/', views.about, name='about'),
    path('round_entry/', views.round_entry, name='round_entry'),
    path('front_9/', views.front_9, name='front_9'),
    path('back_9/', views.back_9, name='back_9'),
]