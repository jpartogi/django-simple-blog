from django.core import urlresolvers

def get_form_target():
    """
    Returns the target URL for the comment form submission view.
    """
    return urlresolvers.reverse("djblog.views.add_comment")