from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from day_9.models import Post
from day_9.permissions import MyCustomPermissionClass
from day_9.serializers import UserSerializer, RegisterSerializer, LoginSerializer, PostSerializer


class UserProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterJWTAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "user_id": user.id,
            "username": user.username,
            "refresh": str(refresh),
            "access": str(access),
        }, status=status.HTTP_201_CREATED)

class LoginJWTAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "user_id": user.id,
            "username": user.username,
            "refresh": str(refresh),
            "access": str(access),
        })


class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermissionClass]
