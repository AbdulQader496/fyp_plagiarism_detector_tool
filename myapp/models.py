import os
from turtle import title
from uuid import uuid4
from django.conf.urls import url
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.fields import AutoField
from numpy import delete
from django.db.models.signals import post_save
from django.dispatch import receiver



User = settings.AUTH_USER_MODEL


class Document(models.Model):
              
    docfile = models.FileField(upload_to='')
    username= models.OneToOneField(User, unique= True, related_name= "usernames" , on_delete=models.CASCADE)   
    fileData = models.TextField()
    title = models.TextField(default="No title")


    def delete(self, *args, **kwargs):
        self.docfile.delete()
        super().delete(*args,**kwargs)

class Class(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    className = models.CharField(max_length=100)
    courseCode = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    semester = models.CharField(max_length=100)
    createdDate = models.DateField(editable=False, auto_now_add=True)
    classID = models.CharField(max_length=100 ,unique=True, default=uuid4, editable=False)

#     @receiver(post_save, sender=User)
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             Class.objects.create(user=instance)

#     @receiver(post_save, sender=User)
#     def save_user_profile(sender, instance, **kwargs):
#         instance.Class.save()        

    def deleteClass(self, *args, **kwargs):
        self.classID.delete()
        super().delete(*args, **kwargs)
        

class Class_fileupload(models.Model):

    classID = models.CharField(max_length=255)
    matricNo = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    class_docfile = models.FileField(upload_to='')
    class_filedata = models.TextField(null=True)

    def delete(self, *args, **kwargs):
        self.class_docfile.delete()
        super().delete(*args,**kwargs)