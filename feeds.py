from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from djblog.models import Entry, Category

class EntriesFeed(Feed):
    feed_type = Atom1Feed
    title = "Blog Feed"
    link = "/blog/"
    description = "Blog Feed"
    #description_template = 'job/feed.html'

    def items(self):
        return Entry.objects.order_by('-posted')[:10]

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return item.creator.username

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