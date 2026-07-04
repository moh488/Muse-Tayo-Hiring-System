from django.db import models
from applicants.models import JobApplication


class OnboardingRecord(models.Model):
    application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='onboarding')
    contract_start_date = models.DateField(null=True, blank=True)
    agreed_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    equipment_assigned = models.BooleanField(default=False)
    safety_training_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Onboarding for {self.application.candidate}"
