from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    age = models.IntegerField()

class Category(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    categories = models.ManyToManyField(Category, related_name="categories")
