from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Category
from apps.post.models import Post
from apps.post.serializers import PostSerializer
from .serializers import CategorySerializer

# Create your views here.
class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.all()

class PostCategoryListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = Category.objects.get(slug=category_slug)
        return Post.objects.filter(category=category, status='active')
