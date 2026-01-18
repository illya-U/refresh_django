from django.urls import path

from day_3.views import debug_request

urlpatterns = [
    path('debug_request/', debug_request),
]