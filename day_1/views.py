from django.views import View
from django.http import HttpResponse

class UsersListView(View):
    def get(self, request):
        return HttpResponse("Users list")
