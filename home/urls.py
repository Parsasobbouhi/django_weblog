from django.urls import path
from . import views

app_name = 'home'

# my urls


urlpatterns = [
    path('', views.home, name='main'),
]
