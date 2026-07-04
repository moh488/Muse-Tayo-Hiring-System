from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import json
from users.permissions import role_required
from django.shortcuts import render
from jobs.models import JobRequisition
from applicants.models import JobApplication
from interviews.models import InterviewSchedule
from users.models import SystemUser


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER', 'INTERVIEWER'])
def index(request):
    today = timezone.now().date()
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_start = today.replace(day=1)

    from applicants.models import JobApplication as RecruiterApp
    from jobs.models import JobApplication as FrontEndApp

    if request.user.role in ('ADMIN', 'HR_MANAGER'):
        is_staff_admin = True
        kpis = {
            'new_jobs': JobRequisition.objects.filter(status='ACTIVE', created_at__gte=week_ago).count(),
            'new_applicants_today': RecruiterApp.objects.filter(applied_date__date=today).count(),
            'hired_this_month': RecruiterApp.objects.filter(stage='HIRED', updated_at__date__gte=month_start).count(),
            'interviews_today': InterviewSchedule.objects.filter(scheduled_time__date=today).count(),
            'pending_verifications': SystemUser.objects.filter(is_verified=False).count(),
            'total_users': SystemUser.objects.filter(is_active=True).count(),
        }

        pipeline = RecruiterApp.objects.values('stage').annotate(count=Count('id')).order_by('stage')
        pipeline_data = {item['stage']: item['count'] for item in pipeline}
        total_apps = sum(pipeline_data.values()) or 1

        selected = pipeline_data.get('SELECTED', 0) + pipeline_data.get('HIRED', 0)
        rejected = pipeline_data.get('REJECTED', 0)
        pending = total_apps - selected - rejected

        pie_data = {
            'selection_rate': round((selected / total_apps) * 100, 1),
            'rejection_rate': round((rejected / total_apps) * 100, 1),
            'pending_rate': round((pending / total_apps) * 100, 1),
        }

        recent_applications = RecruiterApp.objects.select_related('candidate', 'job').order_by('-applied_date')[:10]
        upcoming_interviews = InterviewSchedule.objects.filter(
            scheduled_time__gte=now, status='SCHEDULED'
        ).select_related('application__candidate', 'application__job').order_by('scheduled_time')[:10]
    else:
        is_staff_admin = False
        kpis = {
            'total_jobs_applied': FrontEndApp.objects.filter(user=request.user).count(),
            'selected_applications': RecruiterApp.objects.filter(candidate__email=request.user.email, stage__in=['SELECTED', 'HIRED']).count(),
            'rejected_applications': RecruiterApp.objects.filter(candidate__email=request.user.email, stage='REJECTED').count(),
        }

        pipeline = RecruiterApp.objects.filter(candidate__email=request.user.email).values('stage').annotate(count=Count('id')).order_by('stage')
        pipeline_data = {item['stage']: item['count'] for item in pipeline}
        total_apps = sum(pipeline_data.values()) or 1

        selected = pipeline_data.get('SELECTED', 0) + pipeline_data.get('HIRED', 0)
        rejected = pipeline_data.get('REJECTED', 0)
        pending = total_apps - selected - rejected

        pie_data = {
            'selection_rate': round((selected / total_apps) * 100, 1),
            'rejection_rate': round((rejected / total_apps) * 100, 1),
            'pending_rate': round((pending / total_apps) * 100, 1),
        }

        recent_applications = RecruiterApp.objects.filter(candidate__email=request.user.email).select_related('candidate', 'job').order_by('-applied_date')[:10]
        upcoming_interviews = InterviewSchedule.objects.filter(
            application__candidate__email=request.user.email,
            scheduled_time__gte=now, status='SCHEDULED'
        ).select_related('application__candidate', 'application__job').order_by('scheduled_time')[:10]

    return render(request, 'dashboard/index.html', {
        'is_staff_admin': is_staff_admin,
        'kpis': kpis,
        'pipeline_data': pipeline_data,
        'pipeline_json': json.dumps(pipeline_data),
        'pie_data': pie_data,
        'pie_counts': {'selected': selected, 'rejected': rejected, 'pending': pending},
        'recent_applications': recent_applications,
        'upcoming_interviews': upcoming_interviews,
    })
