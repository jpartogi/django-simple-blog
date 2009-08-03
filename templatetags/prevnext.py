from django.template import Library, Node
from django.db.models import get_model

register = Library()
    
class NextPrevEntryNode(Node):
    def render(self, context):
        entry = context['entry']
        
        next_entry = entry.get_next_entry()
        prev_entry = entry.get_prev_entry()
        
        if next_entry is not None:
            context['next_entry'] = entry.get_next_entry()
        
        if prev_entry is not None:
            context['prev_entry'] = entry.get_prev_entry()
        
        return ''
 
def get_next_prev_entry (parser, token):
    return NextPrevEntryNode()

get_next_prev_entry = register.tag(get_next_prev_entry)