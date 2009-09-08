# $Id: models.py 1d272b240620 2009/09/08 11:37:42 jpartogi $
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tagging.models import Tag

from wmd import models as wmd_models

class Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    sites = models.ManyToManyField(Site)
    picture = models.FileField(upload_to='images/')
    timezone = models.CharField(max_length=50)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=50)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % ( self.slug )

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

class EntryManager(models.Manager):
    def get_prev_entry(self, pk):
        list = self.get_latest_posted_entries().filter(id__gt=pk).reverse()
        if len(list) > 0: return list[0]
        else: return None

    def get_next_entry(self, pk):
        list = self.get_latest_posted_entries().filter(id__lt=pk)
        if len(list) > 0: return list[0]
        else: return None

    def get_latest_posted_entries(self):
        return self.exclude(posted__gte=datetime.datetime.now()).exclude(is_draft=True).order_by('-posted')
    
class Entry(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, verbose_name='category')
    content = wmd_models.MarkDownField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(auto_now_add = True, verbose_name='Created Date')
    updated = models.DateTimeField(auto_now = True, verbose_name='Updated Date')
    posted = models.DateTimeField(verbose_name='Posted Date')
    creator = models.ForeignKey(User)
    sites = models.ManyToManyField(Site)
    tag_list = models.CharField(max_length=128, blank=True, null=True)
    is_draft = models.BooleanField()

    objects = EntryManager()
    
    def __unicode__(self):
        return self.title

    def save(self):
        """
        override save method. to add tag automatically.
        Arguments:
        - `self`:
        """
        super(Entry,self).save()
        self.tags = self.tag_list

    def get_absolute_url(self):
        return "/%s/%s/" % (self.posted.strftime("%Y/%b/%d").lower(), self.slug)

    def get_next_entry(self):
        return self.__class__._default_manager.get_next_entry(self.pk)

    def get_prev_entry(self):
        return self.__class__._default_manager.get_prev_entry(self.pk)

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)

    tags = property(_get_tags, _set_tags)
    
    class Meta:
        verbose_name_plural = 'entries'
        ordering = ['-posted']