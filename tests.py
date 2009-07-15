from django.core import urlresolvers
from django.test import TestCase
from django.test.client import Client

from djblog import *
from djblog.views import *

class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_preview_comment(self):
        url = urlresolvers.reverse('djblog.views.comment.preview')
        logger.debug("URL %s" % url)

        data = {'creator': 'joshua',
            'website': 'http://scrum8.com',
            'email': 'bla@bla.com',
            'comment': 'bla',
            'entry_id': 1,
            'preview': 'Preview Comment',
        }

        response = self.client.post(url,data=data)
        self.assertTemplateUsed(response, 'blog/view.html')

    def test_save_comment(self):
        url = urlresolvers.reverse('djblog.views.comment.save')
        logger.debug("URL %s" % url)