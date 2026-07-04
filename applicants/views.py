from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.permissions import role_required
from applicants.models import JobApplication, Candidate
from applicants.forms import CandidateForm, StageUpdateForm
from jobs.models import JobRequisition


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def applicant_list(request):
    applications = JobApplication.objects.select_related('candidate', 'job').order_by('-applied_date')
    stage_filter = request.GET.get('stage') or request.POST.get('stage')
    job_code = request.GET.get('job_code') or request.POST.get('job_code')
    name = request.GET.get('name') or request.POST.get('name')
    if stage_filter:
        applications = applications.filter(stage=stage_filter)
    if job_code:
        applications = applications.filter(job__reference_code__icontains=job_code)
    if name:
        applications = applications.filter(
            Q(candidate__first_name__icontains=name) | Q(candidate__last_name__icontains=name)
        )
    return render(request, 'applicants/applicant_list.html', {
        'applications': applications,
        'stages': JobApplication.STAGE_CHOICES,
    })


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def applicant_detail(request, pk):
    application = get_object_or_404(
        JobApplication.objects.select_related('candidate', 'job'), pk=pk
    )
    if not application.is_read:
        application.is_read = True
        application.save()
    form = StageUpdateForm(request.POST or None, instance=application)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Application stage updated.')
        return redirect('applicants:applicant_detail', pk=pk)
    return render(request, 'applicants/applicant_detail.html', {
        'application': application,
        'form': form,
    })


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def add_candidate(request):
    jobs = JobRequisition.objects.filter(status='ACTIVE')
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            job_id = request.POST.get('job_id')
            if job_id:
                job = JobRequisition.objects.filter(pk=job_id).first()
                if job:
                    JobApplication.objects.get_or_create(candidate=candidate, job=job)
            messages.success(request, 'Candidate added successfully.')
            return redirect('applicants:applicant_list')
    else:
        form = CandidateForm()
    return render(request, 'applicants/add_candidate.html', {'form': form, 'jobs': jobs})


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def mark_all_read(request):
    """Mark all unread job applications as read, then redirect to applicant list."""
    JobApplication.objects.filter(is_read=False).update(is_read=True)
    return redirect('applicants:applicant_list')


@role_required(['ADMIN', 'HR_MANAGER', 'RECRUITER'])
def update_stage(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        application.stage = request.POST.get('stage', application.stage)
        application.recruiter_notes = request.POST.get('recruiter_notes', '')
        application.save()
        messages.success(request, 'Stage updated successfully.')
    return redirect('applicants:applicant_list')
