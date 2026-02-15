from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from day_9.views import UserProfileViewSet, LoginJWTAPIView, RegisterJWTAPIView, PostRetrieveAPIView

user_router = DefaultRouter()
user_router.register("user_view_set", UserProfileViewSet)

urlpatterns = [
    path('register_jwt/', RegisterJWTAPIView.as_view()),
    path('login_jwt/', LoginJWTAPIView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('posts/<int:pk>/', PostRetrieveAPIView.as_view(), name="order_details"),

    *user_router.urls
]
