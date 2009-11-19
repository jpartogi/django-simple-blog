# $Id: urls.py 36b1b1172a9b 2009/09/08 11:59:50 jpartogi $
from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail, simple
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap

from simple_blog.models import Entry
from simple_blog.feeds import EntriesFeed
from simple_blog.views import entry_list

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

entry_archives_dict = {
    'queryset': queryset,
    'template_object_name': 'entry',
    'date_field': 'posted',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'entries': GenericSitemap(entry_dict, priority=0.6),
}

#TODO: Add comments syndication feed
urlpatterns = patterns('',
    url(r'^category/(?P<category_name>[\w-]+)/$',
        entry_list,
        dict(entry_list_dict),
        name='blog-entries-by-category'),

    url(r'^tag/(?P<tag_name>[\w-]+)/$',
        entry_list,
        dict(entry_list_dict),
        name='blog-entries-by-tag'),

    url(r'^feed/(?P<url>.*)/$',
        'django.contrib.syndication.views.feed',
        {'feed_dict': feeds},
        name='blog-entry-feeds'), 

    url(r'^sitemap.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
        name='blog-sitemap'),

    url(r'^comments/', include('django.contrib.comments.urls')),
    
    url(r'^comment/saved/$',
        simple.direct_to_template,
        {'template': 'comments/saved.html'},
        name='blog-comment-saved'),

    url(r'^archives/',
        list_detail.object_list,
        dict(entry_list_dict, template_name= 'blog/archive.html'),
        name='blog-archives'),

    url(r'^(?P<year>\d{4})/$',
        date_based.archive_year,
        dict(entry_archives_dict, template_name='blog/archives/year.html'),
        name='blog-archives-year'),

    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        date_based.archive_month,
        dict(entry_archives_dict, template_name='blog/archives/month.html'),
        name='blog-archives-month'),

    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
        date_based.archive_day,
        dict(entry_archives_dict, template_name='blog/archives/day.html'),
        name='blog-archives-day'),
        
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\w-]+)/$',
        date_based.object_detail,
        dict(entry_dict, template_name='blog/view.html', slug_field = 'slug',),
        name='blog-view-entry'),
     
    url(r'^$',
        list_detail.object_list,
        dict(entry_list_dict),
        name='blog-entry-list'), #This must be last
)