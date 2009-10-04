# $Id: feeds.py 5ee3537e5395 2009/08/22 11:31:30 jpartogi $
from django.utils.translation import ugettext as _
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site
from django.utils.feedgenerator import Atom1Feed

from djblog.models import Entry, Category

class EntriesFeed(Feed):
    feed_type = Atom1Feed
    description_template = 'blog/feed.html'

    def title(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("%(site_name)s Feed") % dict(site_name=self._site.name)

    def description(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return _("Latest blog entries on %(site_name)s") % dict(site_name=self._site.name)

    def items(self):
        return Entry.objects.get_latest_posted_entries()[:10]

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return item.creator

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.
        """
        return item.posted

    def item_categories(self):
        """
        Returns the categories for every item in the feed.
        """
        return Category.objects.all()

    def link(self):
        if not hasattr(self, '_site'):
            self._site = Site.objects.get_current()
        return "http://%s/" % (self._site.domain)