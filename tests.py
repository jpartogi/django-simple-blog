from django.core import urlresolvers
from django.test import TestCase
from django.test.client import Client

from djblog import *
from djblog.views import *
from djblog.models import *

class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_blog_view(self):
        entry = Entry.objects.get(pk=1)

        params = {'year': '2009','month': '05', 'day': '16', 'slug': 'entry-title'}
        url = urlresolvers.reverse('djblog.views.blog.view', kwargs=params)
        response = self.client.get(url)

        self.assertEqual(entry, response.context['entry'])
        
        self.assertTemplateUsed(response, 'blog/view.html')

    def test_blog_list(self):
        url = urlresolvers.reverse('djblog.views.blog.list')

        response = self.client.get(url)
        self.failUnlessEqual(len(response.context['entries'].object_list), 2)
        
        category = Category.objects.get(pk=1)

        url = urlresolvers.reverse('djblog.views.blog.list', kwargs={'category_name':category.name})

        response = self.client.get(url)
        
        self.failUnlessEqual( len(response.context['entries'].object_list), 1 )

        self.assertTemplateUsed(response, 'blog/list.html')