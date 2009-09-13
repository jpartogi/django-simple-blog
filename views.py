# $Id: views.py 1d272b240620 2009/09/08 11:37:42 jpartogi $
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail

from tagging.models import Tag, TaggedItem

from djblog.forms import *
from djblog.models import *

def entry_list(request, category_name=None, tag_name=None, queryset=None, paginate_by=None,
        template_name=None, template_object_name=None):

    if category_name != None:
        category = get_object_or_404(Category, slug=category_name)
        queryset = queryset.filter(category = category)

    if tag_name != None:
        tag = get_object_or_404(Tag,name=tag_name)
        queryset = TaggedItem.objects.get_by_model(Entry, tag) #TODO:  this causes bug

    queryset.order_by('posted')
    
    return list_detail.object_list(request, queryset, paginate_by=paginate_by,
                                    template_name = template_name,
                                    template_object_name= template_object_name)