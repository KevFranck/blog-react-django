from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from apps.post.models import Post
from apps.notification.models import Notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

# Create your views here.
class CommentPostAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'post_id': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def post(self, request):
        post_id = request.data['post_id']
        name = request.data['name']
        email = request.data['email']
        comment = request.data['comment']

        post = Post.objects.get(id=post_id)

        Comment.objects.create(
            post=post,
            name=name,
            email=email,
            comment=comment
        )

        Notification.objects.create(
            user=post.user,
            post=post,
            type='comment',
        )

        return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)
