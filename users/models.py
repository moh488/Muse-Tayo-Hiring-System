from django.contrib.auth.models import AbstractUser
from django.db import models


class SystemUser(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'System Administrator'),
        ('HR_MANAGER', 'HR Manager'),
        ('RECRUITER', 'Technical Recruiter'),
        ('INTERVIEWER', 'Interviewer/Engineer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RECRUITER')
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
