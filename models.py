from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from tinymce import models as tinymce_models

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
    class Meta:
        verbose_name_plural = 'entries'

class Comment(models.Model):
    creator = models.CharField(max_length=50, verbose_name='Your Name')
    email = models.EmailField()
    website = models.URLField()
    comment = models.TextField()
    posted = models.DateTimeField(verbose_name = 'Posted Date')
    approved = models.BooleanField()
    entry = models.ForeignKey(Entry)