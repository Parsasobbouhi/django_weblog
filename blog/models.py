from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BooleanField
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from unidecode import unidecode
from PIL import Image
from django.core.exceptions import ValidationError


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now=True)
    status = BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'pk': self.id})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ManyToManyField(Category, related_name='articles')
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=5000)
    image = models.ImageField(upload_to='images/articles')
    pub_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, default='')
    status = BooleanField(default=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.title))
            unique_slug = base_slug
            counter = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    body = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.article.title}'

    class Meta:
        ordering = ['-created']


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-created']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} liked {self.article.title}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        unique_together = ('user', 'article')
