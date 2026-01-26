from django.urls import path
from day_4.views import hello_world

urlpatterns = [
    path('hello_world/', hello_world)
]