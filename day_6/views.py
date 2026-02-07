from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from day_6.models import UserProfile, Post, Category
from day_6.serializers import UserProfileSerializer, PostSerializer, CategorySerializer, RemoveCategoryToPostSerializer, \
    RegisterSerializer, LoginSerializer, UserSerializer


@csrf_exempt
def user(request):
    if request.method == "GET":
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(["GET", "POST"])
def posts(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryAPIView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data)


class PostGetFilterAPIView(ListModelMixin, GenericAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        filter_value = self.kwargs.get('filter')
        return Post.objects.filter(title__contains=filter_value)

    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)

class GetCsrfTokenAPIView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def add_category(self, request, pk=None):
        post = self.get_object()
        category_id = request.data.get('category_id', "")
        if not isinstance(category_id, int):
            return Response({'category_id': ['This field is required.']}, status=status.HTTP_400_BAD_REQUEST)
        if Category.objects.filter(pk=category_id).exists():
            post.categories.add(category_id)
        else:
            return Response("this category id is not relevant", status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_category(self, request, pk=None):
        post = self.get_object()
        serializer = RemoveCategoryToPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = serializer.validated_data['category_id']
        if post.categories.filter(pk=category).exists():
            post.categories.remove(category)
        else:
            return Response("this category id is not relevant", status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

# session authentication

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.validated_data['user']
        login(request, user)
        return Response(
            {"message": "User created"},
            status=status.HTTP_201_CREATED
        )

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({"message": "Logged in"})

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})

# token authentication

class RegisterJWTAPIView(APIView):
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password")
        )
        if not user:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "user_id": user.id,
            "username": user.username,
            "refresh": str(refresh),
            "access": str(access),
        })

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get_permissions(self):
        if self.action in [
            'create',
            'list',
            'retrieve',
            'update',
            'destroy',
            'partial_update',
        ]:
            return [IsAdminUser()]
        if self.action in [
            'self_partial_update',
            'self_delete',
            'get_me',
        ]:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=["get"])
    def get_me(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def self_partial_update(self, request):
        user = self.request.user
        serializer = UserSerializer(user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def self_delete(self, request):
        user = self.request.user
        user.delete()
        return Response("user deleted", status=status.HTTP_204_NO_CONTENT)





