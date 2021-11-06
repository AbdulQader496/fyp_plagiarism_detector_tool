from os import access
from django import forms
from django.db import models

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        
        label='Select a file',
        help_text='accept only .txt files.'
    )