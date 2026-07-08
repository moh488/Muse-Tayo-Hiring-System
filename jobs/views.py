import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.permissions import role_required
from jobs.models import JobRequisition, JobApplication
from jobs.forms import JobRequisitionForm
from applicants.models import Candidate


def generate_reference_code():
    return f'MTHS-2026-{random.randint(1000, 9999)}'


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def post_job(request):
    initial = {'reference_code': generate_reference_code()}
    form = JobRequisitionForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        job = form.save(commit=False)
        job.posted_by = request.user
        if not job.reference_code:
            job.reference_code = generate_reference_code()
        job.save()
        messages.success(request, f'Job {job.reference_code} posted successfully.')
        return redirect('jobs:list_jobs')
    return render(request, 'jobs/post_job.html', {'form': form})


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER', 'INTERVIEWER'])
def list_jobs(request):
    jobs = JobRequisition.objects.all().order_by('-created_at')
    status = request.GET.get('status')
    if status:
        jobs = jobs.filter(status=status)
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        action = request.POST.get('action')
        job = get_object_or_404(JobRequisition, pk=job_id)
        if action in ('ACTIVE', 'PAUSED', 'CLOSED'):
            job.status = action
            job.save()
            messages.success(request, f'Job status updated to {action}.')
        return redirect('jobs:list_jobs')
    # 1. Soo qabo dhamaan shaqooyinka uu qofka hadda login-ka ah iska soo codsaday
    applied_job_ids = []
    if request.user.is_authenticated:
        applied_job_ids = JobApplication.objects.filter(user=request.user).values_list('job_id', flat=True)

    # 2. Ku dar liiska context-ga loo dirayo HTML-ka
    return render(request, 'jobs/list_jobs.html', {
        'jobs': jobs,
        'statuses': JobRequisition.STATUS_CHOICES,
        'applied_job_ids': applied_job_ids,  # Khadkan ayaan ku darnay
    })
 



@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobRequisition, id=job_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        location = request.POST.get('location', '')
        education = request.POST.get('education', '')
        phone_number = request.POST.get('phone_number', '') or request.user.phone_number or ''
        email = request.POST.get('email', '') or request.user.email
        experience_years = int(request.POST.get('experience_years', 0) or 0)
        resume = request.FILES.get('resume')

        # 1. Create the front-end JobApplication record
        JobApplication.objects.create(
            job=job,
            user=request.user,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            location=location,
            education=education,
            resume=resume
        )

        # 2. Create/Get the Candidate profile
        name_parts = full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        candidate, _ = Candidate.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone_number,
                'resume': resume,
                'experience_years': experience_years,
                'skills': 'Applied online',
            }
        )

        # 3. Create the recruiter-level JobApplication record
        from applicants.models import JobApplication as RecruiterJobApplication
        RecruiterJobApplication.objects.get_or_create(
            candidate=candidate,
            job=job,
            defaults={
                'stage': 'APPLIED',
            }
        )
        
        messages.success(request, 'Your application has been submitted successfully.')
        return redirect('jobs:list_jobs')  # Dib ugu celi boggii hore ee shaqooyinka
        
    return render(request, 'jobs/apply_form.html', {'job': job})




@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def list_applicants(request):
    # Wuxuu soo qaadayaa dhammaan codsiyada, asagoo soo dhoweynaya xogta shaqada iyo qofka (select_related)
    applications = Candidate.objects.all().order_by('-applied_at')
    stages = Candidate._meta.get_field('status').choices
    context ={
        'applications':applications,
        'stages' : stages
    }
    return render(request, 'applicants/applicant_list.html', context)

@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def view_applicant_detail(request, application_id):
    application = get_object_or_404(Candidate, id=application_id)
    return render(request, 'applicants/applicant_detail.html', {'application': application})
