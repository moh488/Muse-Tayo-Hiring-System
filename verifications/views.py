from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.permissions import role_required
from users.models import SystemUser


@role_required(['ADMIN'])
def pending_approvals(request):
    pending_users = SystemUser.objects.filter(is_verified=False).order_by('-date_registered')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        user = get_object_or_404(SystemUser, pk=user_id)
        if action == 'approve':
            user.is_verified = True
            user.save()
            messages.success(request, f'{user.username} has been approved.')
        elif action == 'decline':
            username = user.username
            user.delete()
            messages.success(request, f'{username} has been declined and removed.')
        return redirect('verifications:pending_approvals')
    return render(request, 'verifications/pending_approvals.html', {'pending_users': pending_users})
