from django import forms
from interviews.models import InterviewSchedule


class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = [
            'application', 'interview_type', 'scheduled_time', 'location_details',
        ]
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class InterviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ['score', 'feedback_notes', 'status']
        widgets = {
            'feedback_notes': forms.Textarea(attrs={'rows': 4}),
            'score': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
