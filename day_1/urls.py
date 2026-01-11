from django.urls import path

from day_1.views import UsersListView

urlpatterns = [
    path('users_list/', UsersListView.as_view()),
]
