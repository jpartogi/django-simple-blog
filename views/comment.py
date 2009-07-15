from django.template import RequestContext
from django.shortcuts import render_to_response

from djblog.forms import *
from djblog.models import *

def preview(request, comment = None, template='blog/view.html'):
    if request.method == 'POST':
        form = CommentForm(request.POST)
         
        data = form.data
        preview = data.get("preview")
        entry_id = data.get("entry_id")
        
        entry = Entry.objects.get(id=entry_id)

        if form.is_valid():
            comment = form.save(commit=False)
            
            if preview != None:
                return render_to_response(template, {
                    'entry': entry,
                    'comment': comment,
                }, context_instance=RequestContext(request))
            else:
                return save(request, comment)
        else:
            return render_to_response(template, {
                'entry': entry,
                'comment': form.instance,
            })

    return render_to_response(template, {
        'entry': entry,
    }, context_instance=RequestContext(request))

def save(request, comment=None, template='comment/saved.html'):

    if request.method == 'POST' and comment==None:
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            
        else:
            return preview(request, comment)

    comment.ipaddress = request.META.get("REMOTE_ADDR", None)
    comment.save()

    return render_to_response(template, {
        'comment': comment,
    }, context_instance=RequestContext(request))

def saved(request, template='comments/saved.html'):
    return render_to_response(template, context_instance=RequestContext(request))