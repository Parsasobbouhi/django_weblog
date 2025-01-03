from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'status', 'views')
    list_editable = ('status',)
    list_filter = ('status',)

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date', 'status')
    list_editable = ('status',)
    list_filter = ('status',)

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'created', 'body')
    list_filter = ('created',)

@admin.register(models.ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'user_email' ,'created', 'message')
    list_filter = ('created',)
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'email'


@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created')
    list_filter = ('created',)
