from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from day_2.models import UserProfile


# Create your views here.

class UsersListView(View):
    def get(self, request):
        users = UserProfile.objects.all()
        return HttpResponse(
            ", ".join(u.username for u in users)
        )

class UsersDetailsView(View):
    def get(self, request):
        age = request.GET.get('age')
        qs = UserProfile.objects.filter(age__gte=10)
        return HttpResponse(
            ", ".join(u.username for u in qs)
        )

def create_user(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')

    username = request.POST.get('username')
    age = request.POST.get('age')

    if not username or not age:
        return HttpResponseBadRequest('username and age are required')

    user = UserProfile.objects.create(
        username=username,
        age=int(age)
    )

    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'age': user.age,
    })









