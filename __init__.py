import logging
import logging.handlers

from django.core import urlresolvers

LOG_FILENAME = '/tmp/log.out'
logger = logging.getLogger('Logger')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)
logger.addHandler(handler)

def get_form_target():
    """
    Returns the target URL for the comment form submission view.
    """
    return urlresolvers.reverse("djblog.views.comment.save")
