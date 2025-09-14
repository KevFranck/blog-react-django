from django.urls import path
from .views import BookmarkView


urlpatterns = [
    path('post/bookmark-post/', BookmarkView.as_view(), name='bookmark-post'),
]
