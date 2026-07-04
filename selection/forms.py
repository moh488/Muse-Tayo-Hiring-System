from django import forms
from selection.models import OnboardingRecord


class OnboardingRecordForm(forms.ModelForm):
    class Meta:
        model = OnboardingRecord
        fields = [
            'contract_start_date', 'agreed_salary',
            'equipment_assigned', 'safety_training_completed',
        ]
        widgets = {
            'contract_start_date': forms.DateInput(attrs={'type': 'date'}),
        }
