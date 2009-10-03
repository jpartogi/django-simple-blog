# $Id: models.py 36b1b1172a9b 2009/09/08 11:59:50 jpartogi $
import datetime
import pytz

from pytz import timezone

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sitemaps import ping_google
from django.utils.translation import ugettext as _

from tagging.models import Tag

from wmd import models as wmd_models

class Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    sites = models.ManyToManyField(Site)
    picture = models.FileField(upload_to='images/', blank=True, null=True)
    timezone = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

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
        return self.exclude(is_draft=True)
    
class Entry(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, verbose_name=_('category'))
    content = wmd_models.MarkDownField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(auto_now_add = True, verbose_name = _('created date'))
    updated = models.DateTimeField(auto_now = True, verbose_name = _('updated date'))
    posted = models.DateTimeField(auto_now_add = True, verbose_name = _('posted date'))
    #edit_posted = models.BooleanField(blank=True, verbose_name = _('edit posted date?'))
    creator = models.ForeignKey(User)
    sites = models.ManyToManyField(Site)
    tag_list = models.CharField(max_length=128, blank=True, null=True, help_text=_('Separate by space'))
    is_draft = models.BooleanField(verbose_name = _('is draft?'))

    objects = EntryManager()
    
    def __unicode__(self):
        return self.title

    def save(self):
        """
        override save method. to add tag automatically.
        Arguments:
        - `self`:
        """
        """
        if self.id == None or self.edit_posted == True:
            site_id = settings.SITE_ID
            site = Site.objects.select_related().get(pk=site_id)
            blog = site.blog_set.all()[0]
            tz = timezone(blog.timezone)

            #replace the timezone first, then convert to utc

            #self.posted = self.posted.replace(tzinfo=tz).astimezone(pytz.utc)
        """
        super(Entry,self).save()
        self.tags = self.tag_list

        try:
             ping_google()
        except Exception:
             # Bare 'except' because we could get a variety
             # of HTTP-related exceptions.
             pass

    def get_absolute_url(self):
        return "/%s/%s/" % (self.created.strftime("%Y/%b/%d").lower(), self.slug)

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