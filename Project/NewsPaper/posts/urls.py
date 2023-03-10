from django.urls import path
from .views import PostList, NewsList, NewsUpdate, PostDetail, ArticlesList, NewsDelete
from .views import PostSearch, NewsCreate, ArticlesCreate, ArticlesUpdate, ArticlesDelete

urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete', NewsDelete.as_view(), name='post_delete'),
   path('articles/', ArticlesList.as_view(), name='articles_list'),
   path('articles/create', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update', ArticlesUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete', ArticlesDelete.as_view(), name='post_delete'),
]