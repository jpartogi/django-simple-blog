# $Id: urls.py 36b1b1172a9b 2009/09/08 11:59:50 jpartogi $
from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail, simple

from djblog.models import Entry
from djblog.feeds import EntriesFeed
from djblog.views import entry_list

feeds = {
    'entries': EntriesFeed,
}

queryset = Entry.objects.get_latest_posted_entries()

entry_dict = {
    'queryset': queryset,
    'date_field': 'posted',
    'template_object_name': 'entry',
}

entry_list_dict = {
    'queryset': queryset,
    'template_name': 'blog/list.html',
    'template_object_name': 'entry',
    'paginate_by': 10,
}

#TODO: Add comments syndication feed
urlpatterns = patterns('',
    (r'^category/(?P<category_name>[\w-]+)/$', entry_list, dict(entry_list_dict) ),
    (r'^tag/(?P<tag_name>[\w-]+)/$', entry_list, dict(entry_list_dict) ),
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, 'djblog-entry-feeds'), #TODO: can not call reverse url
    (r'^comments/', include('django.contrib.comments.urls')),
    
    (r'^comment/saved/$',  simple.direct_to_template, {'template': 'comments/saved.html'}, 'djblog-comment-saved'),
    (r'^(?P<year>\d{4})/$', date_based.archive_year, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', date_based.archive_month, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', date_based.archive_day, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$', date_based.object_detail, dict(entry_dict, template_name='blog/view.html', slug_field = 'slug',)),
    
    #This must be last
    (r'^$', list_detail.object_list, dict(entry_list_dict), 'djblog-entry-list'),
)