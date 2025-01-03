from django.urls import path
from . import views

app_name = 'account'

# my urls


urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about_developer/', views.about_developer, name='about_developer'),
]
