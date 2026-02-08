from rest_framework import serializers

from day_7.models import Post, Category, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'age']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    author = UserProfileSerializer(many=False)

    class Meta:
        model = Post
        fields = ['title', 'author', 'categories']
