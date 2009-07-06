from django import forms
from django.forms import ModelForm

from djblog.models import *

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('posted', 'approved', 'entry', 'ipaddress', )