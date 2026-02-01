from django.urls import path

from day_6.models import Category
from day_6.views import user, posts, post, CategoryAPIView, PostGetFilterAPIView

urlpatterns = [
    path('user/', user),
    path('posts/', posts),
    path('post/<int:pk>/', post),
    path('category/<int:pk>/', CategoryAPIView.as_view()),
    path('post_title/<str:filter>/', PostGetFilterAPIView.as_view())
]