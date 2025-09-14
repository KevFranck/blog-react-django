from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):

    def get_posts_count(self, obj):
        return obj.posts.count()

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'count_posts')
        read_only_fields = ('id',)
