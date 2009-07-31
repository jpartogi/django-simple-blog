from django.conf.urls.defaults import *
from django.views.generic import date_based, list_detail
from djblog.models import Entry
from djblog.feeds import EntriesFeed

feeds = {
    'entries': EntriesFeed,
}

info_dict = {
    'queryset': Entry.objects.order_by('posted'),
    'date_field': 'posted',
}

urlpatterns = patterns('djblog.views.blog',
    (r'^category/(?P<category_name>\S+)/$','list' ),
    #(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[a-z0-9]+\S+)/$','view'),
    (r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>\S+)/$', date_based.object_detail, dict(info_dict, slug_field='slug')),
    (r'^$','list'),
    #(r'^$', date_based.archive_index, dict(info_dict, template_name='djblog/list.html')),
)

urlpatterns += patterns('djblog.views.comment',
    (r'^comment/saved', 'saved'),
)

urlpatterns += patterns('',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),
)
