from django.shortcuts import redirect


def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return redirect('dashboard:index')
