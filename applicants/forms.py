from django import forms
from applicants.models import Candidate, JobApplication


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'resume',
            'portfolio_url', 'experience_years', 'skills',
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['candidate', 'job', 'stage', 'recruiter_notes']
        widgets = {
            'recruiter_notes': forms.Textarea(attrs={'rows': 3}),
        }


class StageUpdateForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['stage', 'recruiter_notes']
        widgets = {
            'recruiter_notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add notes for this stage change...'}),
        }
