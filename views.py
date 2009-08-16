# $Id: views.py 52ab46c677a7 2009/08/12 10:45:28 jpartogi $
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail

from djblog.forms import *
from djblog.models import *

def entry_list(request, category_name=None, queryset=None, paginate_by=None,
        template_name=None, template_object_name=None):

    if category_name!=None:
        category = get_object_or_404(Category, name=category_name)
        queryset = queryset.filter(category = category)
    
    queryset.order_by('posted')
    
    return list_detail.object_list(request, queryset, paginate_by=paginate_by,
                                    template_name = template_name,
                                    template_object_name= template_object_name)