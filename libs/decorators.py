from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden


def login_required_or_403(view_func):
    return user_passes_test(
        lambda u: u.is_authenticated()
    )(view_func)


def is_admin_or_forbiden(view_func, ignore_methods=[]):
    """
    Decorator for views that checks that the user is logged in and is an admin
    member, sending Forbidden otherwise.
    """

    def check(request, *args, **kwargs):
        if request.method in ignore_methods or\
                request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    check.__doc__ = view_func.__doc__
    check.__name__ = view_func.__name__

    return check
