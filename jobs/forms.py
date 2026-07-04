from django import forms
from jobs.models import JobRequisition


class JobRequisitionForm(forms.ModelForm):
    class Meta:
        model = JobRequisition
        fields = [
            'title', 'reference_code', 'department', 'location',
            'description', 'requirements', 'salary_range_min',
            'salary_range_max', 'status', 'deadline',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 5}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
