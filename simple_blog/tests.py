from django.test import TestCase

from simple_blog.models import Entry

class BlogTestCase(TestCase):
    fixtures = ['entries.json']

    def testPreviousNextEntry(self):
        entry = Entry.objects.get(pk=2)

        prev_entry = entry.get_prev_entry()

        self.assertEqual(prev_entry.title, 'Third Entry')

        next_entry = entry.get_next_entry()

        self.assertEqual(next_entry.title, 'First Entry')