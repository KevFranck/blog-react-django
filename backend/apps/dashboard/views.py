from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.post.models import Post
from apps.user.models import User
from apps.bookmark.models import Bookmark
from apps.comment.models import Comment
from apps.category.models import Category
from apps.notification.models import Notification
from apps.user.serializers import AuthorSerializer
from apps.post.serializers import PostSerializer
from apps.category.serializers import CategorySerializer
from apps.notification.serializers import NotificationSerializer
from apps.comment.serializers import CommentSerializer
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

# Create your views here.
class DashboardView(generics.ListAPIView):
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        views = Post.objects.filter(user=user).aggregate(view = Sum('view'))['view']
        posts = Post.objects.filter(user=user).count()
        likes = Post.objects.filter(user=user).aggregate(total_like = Sum('like'))['total_like']
        bookmarks = Bookmark.objects.filter(post__user=user).count()

        return[{
            "views":views,
            "posts":posts,
            "likes":likes,
            "bookmarks":bookmarks,
        }]

    def list(self, reauest, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DasboardPostListsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)
        return Post.objects.filter(user=user).order_by("-id")

class DashboardCommentListsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.all()

class DashboardNotificationListsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = User.objects.get(id=user_id)

        return Notification.objects.filter(is_read=False, user=user)

class DashboardMarkNotiSeenAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'noti_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    def post(self, request):
        noti_id = request.data['noti_id']
        noti = Notification.objects.get(id=noti_id)

        noti.is_read = True
        noti.save()

        return Response({"message": "Noti Marked As Seen"}, status=status.HTTP_200_OK)


class DashboardPostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        print(request.data)
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        content = request.data.get('content')
        category_id = request.data.get('category')
        image = request.data.get('image')
        status = request.data.get('status')

        user = User.objects.get(id=user_id)
        category = Category.objects.get(id=category_id)

        Post.objects.create(
            user=user,
            category=category,
            title=title,
            content=content,
            image=image,
            status=status,
        )
        return Response({"message": "Post Created"}, status=status.HTTP_201_CREATED)

class DashboardPostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        post_id = self.kwargs['post_id']
        user = User.objects.get(id=user_id)
        return Post.objects.get(id=post_id, user=user)

    def update(self, request, *args, **kwargs):
        post_instance = self.get_object()

        title = request.data.get('title')
        content = request.data.get('content')
        category_id = request.data.get('category')
        image = request.data.get('image')
        status = request.data.get('status')

        category = Category.objects.get(id=category_id)

        post_instance.title = title
        post_instance.content = content
        post_instance.category = category
        if image is not None:
            post_instance.image = image
        post_instance.status = status
        post_instance.save()

        return Response({"message": "Post Updated"}, status=status.HTTP_200_OK)
