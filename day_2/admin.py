from django.contrib import admin

from day_2.models import Post, Category, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Post)