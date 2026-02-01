from django.contrib import admin

from day_6.models import UserProfile, Category, Post

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)