from django.template import Library, Node
from django.db.models import get_model

from simple_blog.models import Entry

register = Library()

class LatestContentNode(Node):
    def __init__(self, model, num, varname):
        self.num, self.varname = num, varname
        self.model = get_model(*model.split('.'))

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

def get_latest(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "get_latest tag takes exactly four arguments"
    if bits[3] != 'as':
        raise TemplateSyntaxError, "third argument to get_latest tag must be 'as'"
    return LatestContentNode(bits[1], bits[2], bits[4])

get_latest = register.tag(get_latest)

class LatestEntriesNode(Node):
    def __init__(self, varname, limit=0):
        self.varname = varname
        self.limit = limit

    def render(self, context):
        entries = Entry.objects.get_latest_posted_entries()
        
        if self.limit != None and self.limit != 0:
            entries = entries[:self.limit]

        context[self.varname] = entries
        
        return ''

def get_latest_entries(parser, token):
    bits = token.contents.split()

    return LatestEntriesNode(bits[2], bits[4])

def get_latest_entries_by_year(parser, token):
    bits = token.contents.split()

    return LatestEntriesNode(bits[2])

get_latest_entries = register.tag(get_latest_entries)
get_latest_entries_by_year = register.tag(get_latest_entries_by_year)
