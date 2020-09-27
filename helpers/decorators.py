from functools import wraps

from django.http import Http404


def staff_or_404(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper
