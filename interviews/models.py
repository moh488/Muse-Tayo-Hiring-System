from django.db import models
from django.conf import settings
from applicants.models import JobApplication


class InterviewSchedule(models.Model):
    TYPE_CHOICES = (
        ('PHONE', 'Phone Screen'),
        ('TECHNICAL', 'Technical Review'),
        ('PANEL', 'Panel Interview'),
        ('SITE_VISIT', 'On-Site Practical Evaluation'),
    )
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    )

    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    title = models.CharField(max_length=200)
    interview_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='TECHNICAL')
    scheduled_time = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=45)
    location_details = models.CharField(max_length=255, help_text='Room name, site location, or meet link')
    interviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_interviews')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='SCHEDULED')
    score = models.IntegerField(blank=True, null=True, help_text='Evaluation Score from 1 to 10')
    feedback_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.application.candidate} on {self.scheduled_time.strftime('%Y-%m-%d')}"
