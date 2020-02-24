
from django.urls import path
from . import views

urlpatterns = [
    path('/pollution', views.pollution),
]