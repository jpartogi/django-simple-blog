from django.template import Library, Node
from django.conf import settings

from django.contrib.sites.models import Site

register = Library()

class FlatPagesNode(Node):
    def render(self, context):
        site_id = settings.SITE_ID
        site = Site.objects.get(pk=site_id)

        flatpages = site.flatpage_set.all()
        
        context['flatpages'] = flatpages
        return ''

def get_flatpages(parser, token):
    return FlatPagesNode()

get_flatpages = register.tag(get_flatpages)