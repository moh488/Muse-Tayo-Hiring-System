from django.shortcuts import render
from users.permissions import role_required
from applicants.models import JobApplication
from jobs.models import JobRequisition
from users.models import SystemUser
from backups.utils import export_candidates_to_excel, export_jobs_to_excel, export_summary_pdf


@role_required(['ADMIN'])
def export_panel(request):
    if request.GET.get('export') == 'candidates':
        qs = JobApplication.objects.select_related('candidate', 'job').all()
        return export_candidates_to_excel(qs)
    if request.GET.get('export') == 'jobs':
        return export_jobs_to_excel(JobRequisition.objects.all())
    if request.GET.get('export') == 'users_pdf':
        users = SystemUser.objects.all()
        headers = ['Username', 'Email', 'Role', 'Verified', 'Active']
        rows = [
            [u.username, u.email, u.get_role_display(), u.is_verified, u.is_active]
            for u in users
        ]
        return export_summary_pdf('Muuse Tayo Users Report', headers, rows)
    if request.GET.get('export') == 'applications_pdf':
        apps = JobApplication.objects.select_related('candidate', 'job').all()
        headers = ['Candidate', 'Job', 'Stage', 'Applied Date']
        rows = [
            [str(a.candidate), a.job.title, a.get_stage_display(), a.applied_date.strftime('%Y-%m-%d')]
            for a in apps
        ]
        return export_summary_pdf('Muuse Tayo Applications Report', headers, rows)
    return render(request, 'backups/export_panel.html')
