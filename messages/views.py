from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from messages.models import DirectMessage
from messages.forms import DirectMessageForm
from users.models import SystemUser


def chat_room(request):
    user = request.user
    threads = DirectMessage.objects.filter(
        Q(sender=user) | Q(recipient=user)
    ).select_related('sender', 'recipient').order_by('-timestamp')

    contact_ids = set()
    for msg in threads:
        contact_ids.add(msg.sender_id if msg.sender_id != user.id else msg.recipient_id)

    contacts = SystemUser.objects.filter(id__in=contact_ids, is_active=True)
    active_contact_id = request.GET.get('contact')
    active_contact = None
    conversation = []

    if active_contact_id:
        active_contact = get_object_or_404(SystemUser, pk=active_contact_id)
        conversation = DirectMessage.objects.filter(
            Q(sender=user, recipient=active_contact) | Q(sender=active_contact, recipient=user)
        ).select_related('sender', 'recipient').order_by('timestamp')
        DirectMessage.objects.filter(recipient=user, sender=active_contact, is_read=False).update(is_read=True)

    form = DirectMessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        msg = form.save(commit=False)
        msg.sender = user
        msg.save()
        messages.success(request, 'Message sent.')
        return redirect(f'{request.path}?contact={msg.recipient_id}')

    all_users = SystemUser.objects.filter(is_active=True).exclude(pk=user.pk)
    form.fields['recipient'].queryset = all_users

    return render(request, 'messages/chat_room.html', {
        'contacts': contacts,
        'all_users': all_users,
        'active_contact': active_contact,
        'conversation': conversation,
        'form': form,
    })
