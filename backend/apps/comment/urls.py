from django.urls import path
from .views import CommentPostAPIView


urlpatterns = [
    path('post/comment-post/', CommentPostAPIView.as_view(), name='comment-post'),
]
