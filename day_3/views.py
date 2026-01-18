from doctest import UnexpectedException

from Tools.scripts.highlight import analyze_python
from django.db import transaction
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.views.decorators.csrf import csrf_exempt

from day_3.models import Post, UserProfile


# Create your views here.

@csrf_exempt
def debug_request(request):
   aaa = Post.objects.values('id', 'title')

   bbb = Post.objects.values_list('id', 'title')

   ccc = Post.objects.values_list('id', flat=True)

   Post.objects.filter(id=1).update(title=Concat(F('title'), Value('changed')))

   with transaction.atomic():
      UserProfile.objects.filter(age__exact=10).update(username="Timur")
      transaction.set_rollback(True)

   with transaction.atomic():
      UserProfile.objects.filter(age__exact=10).update(username="Anton")

   ttt = UserProfile.objects.filter(age__exact=10).explain()

   ddd = UserProfile.objects.filter(age__exact=10).explain(verbose=True, analyze=True)


   vvv = 1