
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('homepage', views.homepage),
    path('saved_cities', views.saved_cities)
]