from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from users.forms import SystemUserRegistrationForm, SystemUserCreateForm
from users.models import SystemUser
from users.permissions import role_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if not user.is_verified:
                return redirect('users:pending_approval')
            return redirect('root')
        error = 'Invalid username or password.'
    return render(request, 'users/login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    form = SystemUserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        django_messages.success(request, 'Registration successful. Awaiting admin approval.')
        return redirect('users:login')
    return render(request, 'users/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')


@login_required
def pending_approval_view(request):
    return render(request, 'users/pending_approval.html')


@role_required(['ADMIN'])
def add_user(request):
    form = SystemUserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        django_messages.success(request, 'User created successfully.')
        return redirect('users:user_list')
    return render(request, 'users/add_user.html', {'form': form})


@role_required(['ADMIN'])
def user_list(request):
    users = SystemUser.objects.all().order_by('-date_registered')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(SystemUser, pk=user_id)
        if action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            django_messages.success(request, f'User {user.username} updated.')
        return redirect('users:user_list')
    return render(request, 'users/user_list.html', {'users': users})
