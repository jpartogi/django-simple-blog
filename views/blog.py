from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from djblog.forms import *
from djblog.models import *

def view(request, year, month, day, slug):
    posted = date(int(year), int(month), int(day))
    entry = get_object_or_404(Entry, posted__startswith = posted, slug__iexact = slug)
    
    return render_to_response('blog/view.html', {
        'entry': entry,
        'request': request,
    }, context_instance=RequestContext(request))

def list(request, category_name=None):
    entry_list = Entry.objects.all()
    
    if category_name!=None:
        category = get_object_or_404(Category, name=category_name)
        entry_list = Entry.objects.filter(category = category)

    paginator = Paginator(entry_list, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    
    return render_to_response('blog/list.html', {
        'entries': entries,
        'request': request,
    }, context_instance=RequestContext(request))