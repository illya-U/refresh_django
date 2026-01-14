from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    age = models.IntegerField()
