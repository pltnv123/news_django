from django.urls import path
from .views import PostNewsList, PostNewsDetail, PostSearch, PostUpdate, PostDelete, PostCreate, CategoryListView, \
   subscribe, upgrade_user, unsubscribe
from django.views.decorators.cache import cache_page






urlpatterns = [
   path('', cache_page(1)(PostNewsList.as_view()), name='start_new'),
   path('<int:pk>', cache_page(60*5)(PostNewsDetail.as_view()), name='post_detail'),

   path('search/', PostSearch.as_view(), name='post_search'),

   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path("categories/<int:pk>", CategoryListView.as_view(), name='category_list'),
   path("categories/<int:pk>/subscribe", subscribe, name='subscribe'),
   path("categories/<int:pk>/unsubscribe", unsubscribe, name='unsubscribe'),

   path('upgrade/', upgrade_user, name='account_upgrade'),

]

