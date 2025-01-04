from django.shortcuts import get_object_or_404
from blog import models as blog_models
from account import models as account_models



def recent_articles(request):
    recent_articles = blog_models.Article.objects.filter(status=True).order_by('-pub_date')[:3]
    return {'recent_articles': recent_articles}


def show_categories(request):
    categories = blog_models.Category.objects.filter(status=True)
    return {'categories': categories}


def likes(request):
    if request.user.is_authenticated:
        liked_articles = blog_models.Like.objects.filter(user=request.user)
        liked_article_ids = liked_articles.values_list('article', flat=True)
    else:
        liked_article_ids = []

    return {
        'liked_article_ids': liked_article_ids
    }


def user(request):
    if request.user.is_authenticated:
        user = account_models.Profile.objects.get(user=request.user)
        return {'user': user}
    else:
        return {}

def admin_user(request):
    admin = get_object_or_404(account_models.Profile, id=3)
    return {'admin': admin}
