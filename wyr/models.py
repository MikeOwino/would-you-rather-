from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser, models.Model):
    votes = models.IntegerField(default=0)


class Question(models.Model):
    left = models.CharField(default="Question missing!", max_length=500)
    right = models.CharField(default="Question missing!", max_length=500)
    owner = models.CharField(default="ch1ck3n", max_length=100)
    votes = models.IntegerField(default=0)
    vt_l = models.IntegerField(default=0)
    vt_r = models.IntegerField(default=0)
    vt_l2 = models.IntegerField(default=0)
    vt_r2 = models.IntegerField(default=0)
    q_id = models.IntegerField(default=1)
    approved = models.BooleanField(default=False)
    pub_data = models.CharField(max_length=100, default="2021-04-09")


class Vote(models.Model):
    q_id = models.IntegerField(default=1)
    side = models.CharField(default="left", max_length=10)
    voter = models.CharField(default="", max_length=64)
