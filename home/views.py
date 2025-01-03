from django.shortcuts import render
from blog import models


# Create your views here.

def home(request):
    articles = models.Article.objects.filter(status=True)
    recent_article = models.Article.objects.filter(status=True).order_by('-pub_date')[:3]
    return render(request, 'home/home.html', {'articles': articles, 'recent_article': recent_article})