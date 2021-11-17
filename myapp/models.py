import os
from django.conf.urls import url
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.fields import AutoField


User = settings.AUTH_USER_MODEL


class Document(models.Model):
              
    docfile = models.FileField(upload_to='')
    username= models.OneToOneField(User, unique= True, related_name= "usernames" , on_delete=models.CASCADE)   
    fileData = models.TextField()


    def delete(self, *args, **kwargs):
        self.docfile.delete()
        super().delete(*args,**kwargs)