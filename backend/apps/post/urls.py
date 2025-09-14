from django.urls import path
from .views import PostListView, PostDetailView, LikePostAPIView

urlpatterns = [
    path('post/lists/', PostListView.as_view(), name='post-list'),
    path('post/detail/<title>/', PostDetailView.as_view(), name='post-detail'),
    path('post/like-post/', LikePostAPIView.as_view(), name='like-post')
]
