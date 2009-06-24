from django.conf.urls.defaults import *

urlpatterns = patterns('portal.apps.blog.views',
    (r'^$','list'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d+)/(?P<slug>[a-z0-9]+\S+)/$','view'),
    (r'^(?P<username>\S+)/$','list'),
)