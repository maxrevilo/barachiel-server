"""
    Put this file in a directory called, eg, 'middleware,' inside your django
    project. Make sure to create an __init__.py file in the directory so it can
    be included as a module.

    In settings.py. Then include
        'import.path.to.extend_user_session.ExtendUserSession'
    in MIDDLEWARE_CLASSES in settings.py.

    Based on http://stackoverflow.com/a/11423845/1024693
"""
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class ExtendUserSession(object):
    """
        Extends authenticated user's sessions so they don't have to log back in.
    """
    def process_request(self, request):
        # Only extend the session for auth'd users
        if request.user.is_authenticated():
            now = timezone.now()
            request.session.set_expiry(now + timedelta(seconds=settings.SESSION_COOKIE_AGE))
