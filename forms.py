import datetime

from django import forms
from django.forms import ModelForm

from djblog.models import *
"""
class CommentForm(ModelForm):
    entry_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        exclude = ('posted', 'approved', 'entry', 'ipaddress', )
"""        