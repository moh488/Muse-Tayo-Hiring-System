from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.permissions import role_required
from interviews.models import InterviewSchedule
from interviews.forms import InterviewScheduleForm, InterviewFeedbackForm
from users.models import SystemUser


def check_interview_conflicts(interviewers, scheduled_time, duration_minutes, location, exclude_id=None):
    conflicts = []
    end_time = scheduled_time + timedelta(minutes=duration_minutes)
    for interviewer in interviewers:
        overlapping = InterviewSchedule.objects.filter(
            interviewers=interviewer,
            status__in=['SCHEDULED', 'RESCHEDULED'],
            scheduled_time__lt=end_time,
        ).exclude(pk=exclude_id)
        for existing in overlapping:
            existing_end = existing.scheduled_time + timedelta(minutes=existing.duration_minutes)
            if existing.scheduled_time < end_time and scheduled_time < existing_end:
                conflicts.append(f'{interviewer.username} has a conflicting interview at {existing.scheduled_time}')
    room_conflicts = InterviewSchedule.objects.filter(
        location_details=location,
        status__in=['SCHEDULED', 'RESCHEDULED'],
        scheduled_time__lt=end_time,
    ).exclude(pk=exclude_id)
    for existing in room_conflicts:
        existing_end = existing.scheduled_time + timedelta(minutes=existing.duration_minutes)
        if existing.scheduled_time < end_time and scheduled_time < existing_end:
            conflicts.append(f'Room/location "{location}" is booked at {existing.scheduled_time}')
    return conflicts


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def schedule_interview(request):
    initial = {}
    application_id = request.GET.get('application_id')
    if application_id:
        initial['application'] = application_id
    form = InterviewScheduleForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        interview = form.save(commit=False)
        # Auto-generate a title from the candidate name
        try:
            interview.title = f"Interview - {interview.application.candidate}"
        except Exception:
            interview.title = "Interview"
        conflicts = check_interview_conflicts(
            [],
            form.cleaned_data['scheduled_time'],
            45,
            form.cleaned_data['location_details'],
        )
        if conflicts:
            for c in conflicts:
                messages.error(request, c)
        else:
            interview.save()
            messages.success(request, 'Interview scheduled successfully.')
            return redirect('interviews:interview_list')
    return render(request, 'interviews/schedule_interview.html', {'form': form})


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER', 'INTERVIEWER'])
def interview_list(request):
    if request.user.role == 'INTERVIEWER':
        interviews = InterviewSchedule.objects.filter(interviewers=request.user)
    else:
        interviews = InterviewSchedule.objects.all()
    interviews = interviews.select_related(
        'application__candidate', 'application__job'
    ).prefetch_related('interviewers').order_by('-scheduled_time')

    feedback_forms = {}
    if request.method == 'POST':
        interview_id = request.POST.get('interview_id')
        interview = get_object_or_404(InterviewSchedule, pk=interview_id)
        form = InterviewFeedbackForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted.')
            return redirect('interviews:interview_list')
        feedback_forms[interview_id] = form

    return render(request, 'interviews/interview_list.html', {
        'interviews': interviews,
        'status_choices': InterviewSchedule.STATUS_CHOICES,
    })
