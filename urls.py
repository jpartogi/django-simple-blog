from django.conf.urls.defaults import *

from djblog.feeds import *

feeds = {
    'entries': LatestEntries,
}

urlpatterns = patterns('djblog.views.blog',
    (r'^category/(?P<category_name>\S+)/$','list' ),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[a-z0-9]+\S+)/$','view'),
    (r'^$','list'),
)

urlpatterns += patterns('djblog.views.comment',
    (r'^comment/saved', 'saved'),
)

urlpatterns += patterns('',
    (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),
)