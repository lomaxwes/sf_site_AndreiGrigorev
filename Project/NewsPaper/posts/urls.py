# import subscribe as subscribe
from django import views
from django.urls import path
from .views import PostList, NewsList, NewsUpdate, PostDetail, ArticlesList, NewsDelete, CategoriesList, \
   PostsInCategory, HelloView
from .views import PostSearch, NewsCreate, ArticlesCreate, ArticlesUpdate, ArticlesDelete, subscribe,  unsubscribe, CategoryDetail
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', cache_page(60)(PostList.as_view()), name='post_list'),
   path('hello', HelloView.as_view(), name='hello'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/', cache_page(300)(NewsList.as_view()), name='news_list'),
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete', NewsDelete.as_view(), name='post_delete'),
   path('articles/', cache_page(ArticlesList.as_view()), name='articles_list'),
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update', ArticlesUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete', ArticlesDelete.as_view(), name='post_delete'),
   path('categories/', CategoriesList.as_view(), name='categories'),
   path('categories/<int:pk>/', PostsInCategory.as_view(), name='posts_in_category'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]