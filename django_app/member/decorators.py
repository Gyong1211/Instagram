from django.core.exceptions import PermissionDenied


def anonymous_required(f):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            raise PermissionDenied
        return f(request, *args, **kwargs)

    return wrap
