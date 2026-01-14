from django.urls import path
from day_2.views import UsersListView, create_user, UsersDetailsView

urlpatterns = [
    path('users_list/', UsersListView.as_view()),
    path('create_user/', create_user),
    path('get_specific_user/', UsersDetailsView.as_view())
]