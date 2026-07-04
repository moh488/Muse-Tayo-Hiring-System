from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware:
    EXEMPT_URL_NAMES = ('login', 'register')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            try:
                match = resolve(request.path_info)
                if match.url_name in self.EXEMPT_URL_NAMES:
                    return self.get_response(request)
            except Exception:
                pass
            if request.path.startswith(settings.STATIC_URL) or request.path.startswith(settings.MEDIA_URL):
                return self.get_response(request)
            if request.path.startswith('/admin/'):
                return self.get_response(request)
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)


class VerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_verified:
            try:
                match = resolve(request.path_info)
                allowed = match.namespace == 'users' and match.url_name in ('logout', 'pending_approval', 'login')
            except Exception:
                allowed = False
            if not allowed and not request.path.startswith(settings.MEDIA_URL) and not request.path.startswith(settings.STATIC_URL):
                return redirect('users:pending_approval')
        return self.get_response(request)
