from django.urls import path
from rest_framework.routers import DefaultRouter

from day_7.views import PostGetFilterAPIView, CategoryViewSetAPIView

urlpatterns = [
    path('post/', PostGetFilterAPIView.as_view()),
]

category_router = DefaultRouter()
category_router.register("category_view_set", CategoryViewSetAPIView)

urlpatterns = [*urlpatterns, *category_router.urls]