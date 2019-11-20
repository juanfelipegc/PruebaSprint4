from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('ping', views.ping, name='ping')
]