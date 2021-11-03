from django import forms
from django.db import models

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        
        label='Select a file',
        help_text='accept only .txt, .doc, .docx, .pdf files. Upto 42 MB'
    )