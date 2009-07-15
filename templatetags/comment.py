from django.template import Library, Node

from djblog import get_form_target
from djblog.models import *
from djblog.forms import *

register = Library()

class CommentFormNode(Node):
    def render(self, context):
        entry = context['entry']

        if context['comment'] != None:
            context['commentform'] = CommentForm(instance=context['comment'])
        else:
            context['commentform'] = CommentForm(initial={'entry_id':entry.id})

        context['entry'] = entry
        
        return ''

def render_comment_form(parser, token):
    return CommentFormNode()

def comment_form_target():
    """
    Get the target URL for the comment form.

    Example::

        <form action="{% comment_form_target %}" method="POST">
    """
    return get_form_target()

render_comment_form = register.tag(render_comment_form)
register.simple_tag(comment_form_target)