from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet
from day_7.models import Post, Category
from day_7.paginations import PostCursorPagination
from day_7.serializers import PostSerializer, CategorySerializer
from day_7.throttles import PostGetThrottle


class PostGetFilterAPIView(ListModelMixin, GenericAPIView):
    serializer_class = PostSerializer
    throttle_classes = [PostGetThrottle]

    def get_queryset(self):
        return Post.objects.prefetch_related("categories").select_related("author")

    def get(self, *args, **kwargs):
        return self.list(*args, **kwargs)

class CategoryViewSetAPIView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PostCursorPagination


