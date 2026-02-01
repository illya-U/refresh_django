from rest_framework import serializers

from day_6.models import UserProfile, Post, Category


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'age']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'author', 'categories']

    def validate(self, attrs):
        if attrs["title"] == "title":
            raise serializers.ValidationError("no default title in title")
        return attrs


    def validate_title(self, value):
        if 'specific' in value.lower():
            raise serializers.ValidationError("no specific in post")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']