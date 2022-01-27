from cProfile import label
from dataclasses import field, fields
from msilib.schema import Class
from os import access
from turtle import title
from django import forms
from django.db import models
from myapp.models import Class, Class_fileupload

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        
        label='Select a file',
        help_text='accept only .txt files.'
    ),
    title = forms.CharField(max_length=100),

class ClassForm(forms.ModelForm):

    className = forms.CharField(required=True, label='Enter class name'),
    courseCode = forms.CharField(required=True, label='Enter course code'),
    year = forms.CharField(label='Enter year')
    semester = forms.CharField(label='Enter semester'),
    class Meta:
        model = Class
        fields = ('className','courseCode','year', 'semester')

class Class_FileForm(forms.ModelForm):

    classID = forms.CharField(max_length=255, required=True)
    title = forms.CharField(max_length=100, required=True, label='Enter Title'),
    matricNo = forms.CharField(max_length=100, required=True, label='Enter Matric number'),
    class_docfile = forms.FileField(
        
        label='Select a file',
        help_text='accept only .txt files.'
    ),
    class Meta:
        model = Class_fileupload
        fields = ('classID','title','matricNo','class_docfile')