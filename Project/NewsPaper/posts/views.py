import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author, Category
from .filters import PostFilter
from .forms import PostForm
from pprint import pprint
from django.core.mail import send_mail


class PostList(ListView):
    model = Post
    ordering = '-time_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_posts'] = len(Post.objects.filter())
        return context


class NewsList(ListView):
    model = Post
    queryset = Post.objects.filter(types='NEWS')
    ordering = '-time_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_news'] = len(Post.objects.filter(types='NEWS'))
        return context


class CategoriesList(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'categories.html'
    context_object_name = 'categories'


class PostsInCategory(ListView):
    model = Post
    template_name = 'posts_in_category.html'
    context_object_name = 'posts_in_category'

    def get_queryset(self):
        posts_in_category = Post.objects.filter(category=self.kwargs['pk'])
        return posts_in_category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['cat'] = category
        context['subscribers'] = category.subscribers.all()
        return context


class CategoryDetail(DetailView):
    model = Category
    template_name = 'one_category.html'
    context_object_name = 'one_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['cat'] = category
        context['subscribers'] = category.subscribers.all()
        return context


def subscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return HttpResponseRedirect(reverse('categories'))


def unsubscribe(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return HttpResponseRedirect(reverse('categories'))


class ArticlesList(ListView):
    model = Post
    queryset = Post.objects.filter(types='ARTI')
    ordering = '-time_date'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_of_articles'] = len(Post.objects.filter(types='ARTI'))
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pprint(context)
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_date'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('posts.add_post', 'posts.can_post' )
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ArticlesCreate(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = ('posts.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.types = 'ARTI'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('posts.change_post', 'posts.change_post_category',)
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_template_names(self):
        post = self.get_object()
        # pprint(self)
        # print(post.author)
        # print(post.types)
        if post.types == 'NEWS' and post.author == self.request.user.author:
            self.template_name = 'news_edit.html'
            return self.template_name
        else:
            self.template_name = '404.html'
            return self.template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ArticlesUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('posts.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'

    def get_template_names(self):
        post = self.get_object()
        if post.types == 'ARTI' and post.author == self.request.user.author:
            self.template_name = 'articles_edit.html'
        else:
            self.template_name = '404.html'
        return self.template_name


class NewsDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = ('posts.delete_post', )
    model = Post
    # template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.types == 'NEWS' and post.author == self.request.user.author:
            self.template_name = 'post_delete.html'
            return self.template_name
        else:
            self.template_name = '404.html'
            return self.template_name


class ArticlesDelete(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = ('posts.delete_post', )
    model = Post
    # template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_template_names(self):
        post = self.get_object()
        if post.types == 'ARTI' and post.author == self.request.user.author:
            self.template_name = 'post_delete.html'
        else:
            self.template_name = '404.html'
        return self.template_name

