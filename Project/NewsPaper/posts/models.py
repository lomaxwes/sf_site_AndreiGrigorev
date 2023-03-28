import datetime

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(author_id=self.pk).aggregate(rating=Sum('rating'))['rating']
        rating_comments_author = Comment.objects.filter(user_id=self.user).aggregate(comment_rating=Sum('comment_rating'))['comment_rating']
        rating_comments_posts = Comment.objects.filter(post__author__user=self.user).aggregate(comment_rating=Sum('comment_rating'))['comment_rating']
        self.user_rating = rating_posts_author * 3 + rating_comments_author + rating_comments_posts
        self.save()


class Category(models.Model):
    sport = 'SP'
    politics = 'PO'
    education = 'ED'
    weather = 'WE'

    CATEGORY_TYPES = [
        (sport, 'Спорт'),
        (politics, 'Политика'),
        (education, 'Образование'),
        (weather, 'Погода'),
    ]

    category_name = models.CharField(max_length=2, choices=CATEGORY_TYPES, default=sport, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscriber')

    def __str__(self):
        return self.get_category_name_display()


class CategorySubscriber(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    article = 'ARTI'
    news = 'NEWS'

    POST_TYPE = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    types = models.CharField(max_length=4, choices=POST_TYPE, default=news)
    time_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=False)
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.content[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title.title()}: {self.content}'

    # После создания страницы джанго вернёт нас на страницу котороя прописана ниже
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=False)
    comment_create = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1
        self.save()
        return self.comment_rating
