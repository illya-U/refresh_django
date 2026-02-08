from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.pagination import CursorPagination

class DefaultPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 5

class CustomPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 5

class PostCursorPagination(CursorPagination):
    page_size = 3
    ordering = "-created_at"