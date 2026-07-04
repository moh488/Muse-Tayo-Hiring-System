from messages.models import DirectMessage
from applicants.models import JobApplication


def unread_message_count(request):
    if request.user.is_authenticated:
        # Unread direct messages — shown on the Messages nav link
        msg_count = DirectMessage.objects.filter(recipient=request.user, is_read=False).count()

        # Unread job applications — shown on the bell 🔔 and Applicants nav link (Admin/HR only)
        app_count = 0
        if hasattr(request.user, 'role') and request.user.role in ('ADMIN', 'HR_MANAGER', 'RECRUITER'):
            try:
                app_count = JobApplication.objects.filter(is_read=False).count()
            except Exception:
                app_count = 0

        return {
            'unread_message_count': msg_count,       # for Messages nav badge
            'unread_application_count': app_count,   # for Applicants nav badge + bell
        }
    return {
        'unread_message_count': 0,
        'unread_application_count': 0,
    }
