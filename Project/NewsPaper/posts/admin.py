import apscheduler as apscheduler
from django.contrib import admin
from .models import Category, Post, Author, PostCategory, CategorySubscriber

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(CategorySubscriber)
