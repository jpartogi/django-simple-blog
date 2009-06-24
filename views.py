from datetime import date

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User

from djblog.models import *

def view(request, year, month, day, slug):
    posted = date(int(year), int(month), int(day))
    entry = get_object_or_404(Entry, posted__startswith = posted, slug__iexact = slug)
    return render_to_response('blog/view.html', {
        'entry': entry,
        'request' : request
    }, context_instance=RequestContext(request))

def list(request, username=None):
    if username != None:
        member = get_object_or_404(User, username=username)
        entries = Entry.objects.filter(creator=member).order_by('-posted')
    else:
        entries = Entry.objects.all().order_by('-posted')

    paginator = Paginator(entries, 10)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        entry_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entry_list = paginator.page(paginator.num_pages)

    return render_to_response('blog/list.html', {
        'entry_list': entry_list,
        'request' : request
    }, context_instance=RequestContext(request))