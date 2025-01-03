from django.urls import path
from . import views

app_name = 'blog'

# my urls


urlpatterns = [
    path('list', views.article_list, name='article_list'),
    path('detail/<slug:slug>', views.article_detail, name='article_detail'),
    path('category/<int:pk>', views.category_detail, name='category_detail'),
    path('search', views.search, name='article_search'),
    path('author/<int:pk>', views.author_detail, name='author_detail'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('like/<slug:slug>/<int:pk>', views.like, name='like'),
    path('create_blog', views.create_blog, name='create_blog'),
]
