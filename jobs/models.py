from django.db import models
from django.conf import settings


class JobRequisition(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE', 'Active/Published'),
        ('PAUSED', 'Paused'),
        ('CLOSED', 'Closed'),
    )

    DEPARTMENT_CHOICES = (
        ('CIVIL', 'Civil Engineering'),
        ('MEP', 'Mechanical, Electrical & Plumbing'),
        ('ARCH', 'Architecture & Design'),
        ('SAFETY', 'Health, Safety & Environment (HSE)'),
        ('ADMIN', 'Finance & Administration'),
    )

    title = models.CharField(max_length=255)
    reference_code = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    location = models.CharField(max_length=255, default='Hargeisa Office')
    description = models.TextField()
    requirements = models.TextField()
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_jobs'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return f"{self.reference_code} - {self.title}"


# ================= KU DAR KAN HOOSE =================

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    )

    job = models.ForeignKey(JobRequisition, on_delete=models.CASCADE, related_name='jobs_applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    education = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    applied_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} for {self.job.title}"

