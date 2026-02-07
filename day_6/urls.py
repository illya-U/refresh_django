from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from day_6.models import Category
from day_6.views import user, posts, post, CategoryAPIView, PostGetFilterAPIView, PostViewSet, RegisterAPIView, \
    LoginAPIView, LogoutAPIView, GetCsrfTokenAPIView, UserViewSet, RegisterJWTAPIView, LoginJWTAPIView

urlpatterns = [
    path('user/', user),
    path('posts/', posts),
    path('post/<int:pk>/', post),
    path('category/<int:pk>/', CategoryAPIView.as_view()),
    path('post_title/<str:filter>/', PostGetFilterAPIView.as_view()),
    path('get_csrf_token/', GetCsrfTokenAPIView.as_view()),
    # session authentication
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    # token authentication
    path('register_jwt/', RegisterJWTAPIView.as_view()),
    path('login_jwt/', LoginJWTAPIView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

post_router = DefaultRouter()
post_router.register(r'posts_view_set', PostViewSet)


user_router = DefaultRouter()
user_router.register(r'user_view_set', UserViewSet)

urlpatterns = [*urlpatterns, *post_router.urls , *user_router.urls]
