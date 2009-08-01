from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail
from djblog.models import Entry
from djblog.feeds import EntriesFeed

feeds = {
    'entries': EntriesFeed,
}

queryset = Entry.objects.exclude(is_draft=True).order_by('posted')

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

urlpatterns = patterns('djblog.views.blog',
    (r'^category/(?P<category_name>\S+)/$','list' ),
    (r'^(?P<year>\d{4})/$', date_based.archive_year, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', date_based.archive_month, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', date_based.archive_day, dict(entry_dict, template_name='blog/archives.html')),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>\S+)/$', date_based.object_detail, dict(entry_dict, template_name='blog/view.html', slug_field = 'slug',)),
    (r'^$', list_detail.object_list, dict(entry_list_dict), 'djblog-blog-list'),
)

urlpatterns += patterns('djblog.views.comment',
    (r'^comment/saved', 'saved'),
)

urlpatterns += patterns('',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),
)
