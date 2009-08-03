from django.template import Library, Node
from django.db.models import get_model

register = Library()

class PrevEntryNode(Node):
    def render(self, context):
        entry = context['entry']
        prev_entry = entry.get_prev_entry()
        
        if prev_entry is not None: 
            return prev_entry
        else:
            return ''

def prev_entry(parser, token):
    return PrevEntryNode()

class NextEntryNode(Node):
    def render(self, context):
        entry = context['entry']
        next_entry = entry.get_next_entry()
        
        if next_entry is not None:
            return next_entry
        return ''
    
def next_entry(parser, token):
    return NextEntryNode()

prev_entry = register.tag(prev_entry)
next_entry = register.tag(next_entry)