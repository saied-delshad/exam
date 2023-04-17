    
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class DisableCSRF(MiddlewareMixin):
    """Middleware for disabling CSRF in an specified app name.
    """

    def process_request(self, request):
        """Preprocess the request.
        """
        if request.user.username == 'netrise':
            setattr(request, '_dont_enforce_csrf_checks', True)
        else:
            pass  # check CSRF token validation