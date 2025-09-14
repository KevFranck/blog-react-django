from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Post
from .serializers import PostSerializer
from apps.user.models import User
from apps.notification.models import Notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Post.objects.all().filter(status='active').order_by('-created_at')

class PostDetailView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        title = self.kwargs['title']
        post = Post.objects.get(title=title, status='active')
        post.view += 1
        post.save()
        return post


class LikePostAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post_id')

        user = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)

            Notification.objects.create(
                user=post.user,
                post=post,
                type='like',
            )
            return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)
