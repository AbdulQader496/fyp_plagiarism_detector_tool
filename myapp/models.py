import os
from django.conf.urls import url
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Document(models.Model):        
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    username= models.OneToOneField(User, unique= True, related_name= "usernames" , on_delete=models.CASCADE)   

    def delete(self, *args, **kwargs):
        self.docfile.delete()
        super().delete(*args,**kwargs)