from django.db.models import Count
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from day_2.models import UserProfile, Post, Category


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

@csrf_exempt
def debug_request(request):
    user_1 = UserProfile.objects.get(id=1)
    posts_from_first_user = user_1.posts.all()

    all_messages_from_first_user = [post.title for post in  posts_from_first_user]

    users = UserProfile.objects.prefetch_related("posts")

    for user in users:
        print(user.posts.all())

    UserProfile.objects.annotate(
        post_count=Count("posts")
    )

    posts = Post.objects.select_related('author')
    aaa = [post.author.id for post in posts]

    users = UserProfile.objects.prefetch_related('posts')
    bbb = [user.posts.all() for user in users]

    posts = Post.objects.prefetch_related("categories")
    ccc = [post.categories.all() for post in posts]

    categories = Category.objects.prefetch_related("categories")
    ddd = [category.categories.all() for category in categories]

    posts = Post.objects.annotate(
        categories_count=Count("categories", distinct=True)
    )

    eee = [post.categories_count for post in posts]

    posts = Post.objects.all()

    print("111")

    for post in posts:
        print(post.author.username)



    aaa = 1












