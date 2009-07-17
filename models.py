import datetime

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tinymce import models as tinymce_models

class Blog(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/category/%s/" % ( self.name )

    class Meta:
        verbose_name_plural = 'categories'
        
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
    """
    
    title = models.CharField(max_length=128)
    content = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(verbose_name='Created Date')
    posted = models.DateTimeField(verbose_name='Posted Date')
    category = models.ForeignKey(Category, verbose_name='category')
    creator = models.ForeignKey(User)
    sites = models.ManyToManyField(Site)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/%s/%s/%s/%s/" % (self.posted.strftime("%Y"), \
                                  self.posted.strftime("%m"), \
                                  self.posted.strftime("%d"), \
                                  self.slug)

    def save(self,force_insert=False, force_update=False):
        if self.pk == None:
            self.created = datetime.datetime.now()
        super(Entry, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = 'entries'

class Comment(models.Model):
    creator = models.CharField(max_length=50, verbose_name='Your Name')
    email = models.EmailField()
    website = models.URLField(null=True)
    comment = models.TextField()
    posted = models.DateTimeField(verbose_name = 'Posted Date')
    approved = models.BooleanField(default=False)
    entry_id = models.IntegerField(Entry)
    ipaddress = models.IPAddressField()

    def save(self):
        self.posted = datetime.datetime.now()
        super(Comment,self).save()