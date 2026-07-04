from django.db.models import Count, Avg
from django.shortcuts import render
from users.permissions import role_required
from applicants.models import JobApplication
from jobs.models import JobRequisition


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER', 'INTERVIEWER'])
def analytics_dashboard(request):
    from jobs.models import JobApplication as FrontEndApp
    from applicants.models import JobApplication as RecruiterApp

    if request.user.role in ('ADMIN', 'HR_MANAGER'):
        funnel = RecruiterApp.objects.values('stage').annotate(count=Count('id')).order_by('stage')
        funnel_data = {item['stage']: item['count'] for item in funnel}

        dept_breakdown = RecruiterApp.objects.values(
            'job__department'
        ).annotate(count=Count('id')).order_by('-count')

        hired_apps = RecruiterApp.objects.filter(stage='HIRED').select_related('job')
        time_to_hire_data = []
        total_days = 0
        count = 0
        for app in hired_apps:
            days = (app.updated_at - app.job.created_at).days
            time_to_hire_data.append({
                'candidate': str(app.candidate),
                'job': app.job.title,
                'days': days,
            })
            total_days += days
            count += 1
        avg_time_to_hire = round(total_days / count, 1) if count else 0

        job_stats = {
            'total_jobs': JobRequisition.objects.count(),
            'active_jobs': JobRequisition.objects.filter(status='ACTIVE').count(),
            'total_applications': RecruiterApp.objects.count(),
        }
    else:
        funnel = RecruiterApp.objects.filter(candidate__email=request.user.email).values('stage').annotate(count=Count('id')).order_by('stage')
        funnel_data = {item['stage']: item['count'] for item in funnel}

        dept_breakdown = RecruiterApp.objects.filter(candidate__email=request.user.email).values(
            'job__department'
        ).annotate(count=Count('id')).order_by('-count')

        hired_apps = RecruiterApp.objects.filter(candidate__email=request.user.email, stage='HIRED').select_related('job')
        time_to_hire_data = []
        total_days = 0
        count = 0
        for app in hired_apps:
            days = (app.updated_at - app.job.created_at).days
            time_to_hire_data.append({
                'candidate': str(app.candidate),
                'job': app.job.title,
                'days': days,
            })
            total_days += days
            count += 1
        avg_time_to_hire = round(total_days / count, 1) if count else 0

        job_stats = {
            'total_jobs': FrontEndApp.objects.filter(user=request.user).count(),
            'active_jobs': FrontEndApp.objects.filter(user=request.user, job__status='ACTIVE').count(),
            'total_applications': FrontEndApp.objects.filter(user=request.user).count(),
        }

    return render(request, 'reports/analytics_dashboard.html', {
        'funnel_data': funnel_data,
        'dept_breakdown': dept_breakdown,
        'time_to_hire_data': time_to_hire_data,
        'avg_time_to_hire': avg_time_to_hire,
        'job_stats': job_stats,
    })
