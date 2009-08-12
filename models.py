# $Id: models.py 52ab46c677a7 2009/08/12 10:45:28 jpartogi $
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    sites = models.ManyToManyField(Site)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % ( self.name )

    class Meta:
        verbose_name_plural = 'categories'


class EntryManager(models.Manager):
    def get_next_entry(self, pk):
        list = self.filter(id__gt=pk)
        if len(list) > 0: return list[0]
        else: return None

    def get_prev_entry(self, pk):
        list = self.filter(id__lt=pk).reverse()
        if len(list) > 0: return list[0]
        else: return None
    
class Entry(models.Model):
    """
    These are the backend logics.
    
    When we save if the data is new, then save created date once
    # Create category first
    >>> user = User.objects.get(pk=1)
    >>> category = Category.objects.get(pk=1)
    >>> entry = Entry.objects.create(title='test', content='test', slug='slug', category=category, posted=datetime.datetime.now(), creator=user)
    >>> entry.save()
    >>> entry.title = 'changed'
    >>> cls = entry.__class__
    >>> print entry.get_next_entry()
    None
    >>> print entry.get_prev_entry()
    Second Entry Title
    """    
    title = models.CharField(max_length=128)
    content = models.TextField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(auto_now_add = True, verbose_name='Created Date')
    updated = models.DateTimeField(auto_now = True, verbose_name='Updated Date')
    posted = models.DateTimeField(verbose_name='Posted Date')
    category = models.ForeignKey(Category, verbose_name='category')
    creator = models.ForeignKey(User)
    sites = models.ManyToManyField(Site)
    is_draft = models.BooleanField()

    objects = EntryManager()
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/" % (self.posted.strftime("%Y/%b/%d").lower(), self.slug)

    def get_next_entry(self):
        return self.__class__._default_manager.get_next_entry(self.pk)

    def get_prev_entry(self):
        return self.__class__._default_manager.get_prev_entry(self.pk)

    class Meta:
        verbose_name_plural = 'entries'  