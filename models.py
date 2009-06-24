from django.db import models
from django.contrib.auth.models import User

from tinymce import models as tinymce_models

class Entry(models.Model):
    title = models.CharField(max_length=128)
    content = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=50)
    created = models.DateTimeField(verbose_name='Created Date')
    posted = models.DateTimeField(verbose_name='Posted Date')
    category = models.ForeignKey('common.Category', verbose_name='category')
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/blog/%s/%s/%s/%s/" % (     self.posted.strftime("%Y"), \
                                            self.posted.strftime("%m"), \
                                            self.posted.strftime("%d"), \
                                            self.slug)
    class Meta:
        verbose_name_plural = 'entries'