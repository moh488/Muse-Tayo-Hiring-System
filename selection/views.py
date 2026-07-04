from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from users.permissions import role_required
from applicants.models import JobApplication
from selection.models import OnboardingRecord
from selection.forms import OnboardingRecordForm


@role_required(['ADMIN', 'HR_MANAGER'])
def selected_candidates(request):
    applications = JobApplication.objects.filter(
        stage__in=['SELECTED', 'HIRED']
    ).select_related('candidate', 'job').order_by('-updated_at')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        application = get_object_or_404(JobApplication, pk=app_id)
        onboarding, _ = OnboardingRecord.objects.get_or_create(application=application)
        onboarding.contract_start_date = request.POST.get('contract_start_date') or None
        onboarding.agreed_salary = request.POST.get('agreed_salary') or None
        onboarding.equipment_assigned = request.POST.get('equipment_assigned') == 'on'
        onboarding.safety_training_completed = request.POST.get('safety_training_completed') == 'on'
        onboarding.save()
        messages.success(request, 'Onboarding record updated.')
        return redirect('selection:selected_candidates')

    onboarding_map = {
        ob.application_id: ob
        for ob in OnboardingRecord.objects.filter(application__in=applications)
    }
    app_rows = [
        {'application': app, 'onboarding': onboarding_map.get(app.id)}
        for app in applications
    ]

    return render(request, 'selection/selected_candidates.html', {
        'app_rows': app_rows,
    })
