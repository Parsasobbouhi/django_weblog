from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.core.paginator import Paginator
from . import forms


# Create your views here.
def article_list(request):
    articles = models.Article.objects.filter(status=True)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug):
    article = get_object_or_404(models.Article, slug=slug)
    is_like = models.Like.objects.filter(article=article,
                                         user=request.user).exists() if request.user.is_authenticated else False


    cookie_name = f'viewed_article_{article.id}'
    if not request.COOKIES.get(cookie_name):
        article.views += 1
        article.save()

    if request.method == 'POST':
        body = request.POST.get('body')
        parent_id = request.POST.get('parent_id')
        if request.user.is_authenticated:
            models.Comment.objects.create(article=article, user=request.user, body=body, parent_id=parent_id)


    response = render(request, 'blog/article-details.html', {
        'article': article,
        'is_like': is_like,
    })
    response.set_cookie(cookie_name, 'true', max_age=86400)  # کوکی برای 24 ساعت معتبر است
    return response


def category_detail(request, pk=None):
    category = get_object_or_404(models.Category, id=pk, status=True)
    articles = category.articles.filter(status=True)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    return render(request, 'blog/category-detail.html', {'articles': articles, 'category': category})


def search(request):
    query = request.GET.get('search')
    articles = models.Article.objects.filter(title__contains=query, status=True)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    return render(request, 'blog/article_list.html', {'articles': articles})


def author_detail(request, pk=None):
    author = User.objects.get(id=pk)
    articles = author.articles.filter(status=True)
    paginator = Paginator(articles, 2)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)
    return render(request, 'blog/author_detail.html', {'articles': articles, 'author': author})


def contact_us(request):
    if request.method == 'POST':
        form = forms.ContactUsForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    else:
        form = forms.ContactUsForm()
    return render(request, 'blog/contact_us.html', {'form': form})


def like(request, slug, pk):
    if request.user.is_authenticated:
        try:
            like = models.Like.objects.get(article__slug=slug, user_id=request.user.id)
            like.delete()
            return JsonResponse({'response': 'unliked'})
        except:
            models.Like.objects.create(article_id=pk, user_id=request.user.id)
            return JsonResponse({'response': 'liked'})

def create_blog(request):
    if request.method == 'POST':
        form = forms.CreateBlog(data=request.POST, files=request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            form.save_m2m()
            return redirect('blog:article_list')
    else:
        form = forms.CreateBlog()
    return render(request, 'blog/create_blog.html', {'form': form})
