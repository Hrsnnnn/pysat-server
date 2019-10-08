from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    telphone = models.CharField(max_length=11)
    
    realname = models.CharField(max_length=32)
    school = models.CharField(max_length=64)

    permission = models.IntegerField()

class EntryLog(models.Model):
    userid = models.IntegerField()
    key = models.CharField(max_length=128)
    deadtime = models.DateTimeField()