from functools import wraps
from django.http import HttpResponseForbidden


ROLE_ACCESS = {
    'ADMIN': {
        'dashboard', 'jobs', 'applicants', 'selection', 'interviews',
        'messages', 'users', 'verifications', 'reports', 'backups',
    },
    'HR_MANAGER': {
        'dashboard', 'jobs', 'applicants', 'selection', 'interviews',
        'messages', 'reports',
    },
    'RECRUITER': {
        'dashboard', 'jobs', 'messages', 'reports',
    },
    'INTERVIEWER': {
        'dashboard', 'jobs', 'messages', 'reports',
    },
}


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden('Authentication required.')
            if request.user.role == 'ADMIN' or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('You do not have permission to access this module.')
        return wrapper
    return decorator


def module_allowed(user, module_name):
    if not user.is_authenticated:
        return False
    if user.role == 'ADMIN':
        return True
    return module_name in ROLE_ACCESS.get(user.role, set())
