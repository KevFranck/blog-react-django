from django.urls import path
from .views import CategoryListView, PostCategoryListView

urlpatterns = [
    path('post/categories/list/', CategoryListView.as_view(), name='category-list'),
    path('post/category/posts/<category_slug>/', PostCategoryListView.as_view(), name='post-category-list'),
]
