from django.db import models
from jobs.models import JobRequisition


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    portfolio_url = models.URLField(blank=True, null=True)
    experience_years = models.IntegerField()
    skills = models.TextField()
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class JobApplication(models.Model):
    STAGE_CHOICES = (
        ('APPLIED', 'Newly Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEWING', 'Interview Stage'),
        ('SELECTED', 'Selected/Offer Made'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    )

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(JobRequisition, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='APPLIED')
    recruiter_notes = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate} applying for {self.job.title} - Status: {self.stage}"

    @property
    def full_name(self):
        return f"{self.candidate.first_name} {self.candidate.last_name}"

    @property
    def email(self):
        return self.candidate.email

    @property
    def phone_number(self):
        return self.candidate.phone

    @property
    def resume(self):
        return self.candidate.resume

    @property
    def location(self):
        return "N/A"

    @property
    def education(self):
        return "N/A"

    @property
    def user_account(self):
        from users.models import SystemUser
        return SystemUser.objects.filter(email=self.candidate.email).first()

