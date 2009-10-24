# $Id: categories.py 624acba9a72d 2009/08/18 10:54:51 jpartogi $

from django.template import Library, Node

from simple_blog.models import Category

register = Library()

class CategoriesNode(Node):
    def render(self, context):
        context['categories'] = Category.objects.all()
        return ''

def get_categories(parser, token):
    return CategoriesNode()

get_categories = register.tag(get_categories)