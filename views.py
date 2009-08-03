from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic import list_detail

from djblog.forms import *
from djblog.models import *

def entry_list(request, category_name=None):
    queryset = Entry.objects.all()
    
    if category_name!=None:
        category = get_object_or_404(Category, name=category_name)
        queryset = Entry.objects.filter(category = category)
    
    queryset.order_by('posted')
    
    return list_detail.object_list(request, queryset, paginate_by=10, template_name ='blog/list.html',
                                   template_object_name= 'entry')