
from django.contrib import admin
from django.db.models import F

from .models import UserProfile, Post, Category


def make_adult(modeladmin, request, queryset):
    queryset.update(age=F('age') + 1)


make_adult.short_description = "Increase age by 1"

class PostInline(admin.StackedInline):
    model = Post
    extra = 0

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'is_middle_age')
    list_filter = ('age', 'username')
    search_fields = ('username',)
    actions = [make_adult]
    inlines = [PostInline]

    def is_middle_age(self, obj):
        return 30 <= obj.age <= 40

    is_middle_age.boolean = True
    is_middle_age.short_description = 'Middle age'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass