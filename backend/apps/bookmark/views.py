from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bookmark
from apps.post.models import Post
from apps.user.models import User
from apps.notification.models import Notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

# Create your views here.
class BookmarkView(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        post_id = request.data['post_id']

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        bookmark = Bookmark.objects.filter(user=user, post=post).first()

        if bookmark:
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=status.HTTP_200_OK)
        else:
            Bookmark.objects.create(
                user=user,
                post=post
            )
            Notification.objects.create(
                user=post.user,
                post=post,
                type='bookmark',
            )
            return Response({"message": "Bookmark added"}, status=status.HTTP_201_CREATED)
