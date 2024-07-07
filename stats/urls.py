from django.urls import path
from stats import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/login/', views.login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout', views.user_logout, name="logout"),
    path("name/<name>", views.name, name="name"),
    path('about/', views.about, name='about'),
    path('round_entry/', views.round_entry, name='round_entry'),
    path('front_9/', views.front_9, name='front_9'),
    path('back_9/', views.back_9, name='back_9')
]