import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muuse_tayo_project.settings')
django.setup()

from jobs.models import JobApplication as FrontEndApp
from applicants.models import Candidate, JobApplication as RecruiterApp

def backfill():
    print("Starting candidate backfill...")
    frontend_apps = FrontEndApp.objects.all()
    count = 0
    for f_app in frontend_apps:
        name_parts = f_app.full_name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # 1. Get or create Candidate profile
        candidate, c_created = Candidate.objects.get_or_create(
            email=f_app.email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'phone': f_app.phone_number,
                'resume': f_app.resume,
                'experience_years': 0,
                'skills': 'Applied online',
            }
        )
        if c_created:
            print(f"Created candidate: {candidate.first_name} {candidate.last_name}")
            
        # 2. Get or create recruiter JobApplication
        rec_app, r_created = RecruiterApp.objects.get_or_create(
            candidate=candidate,
            job=f_app.job,
            defaults={
                'stage': 'APPLIED',
            }
        )
        if r_created:
            print(f"Linked application for {candidate.first_name} to job: {f_app.job.title}")
            count += 1
            
    print(f"Backfill complete. Linked {count} new recruitment workflows.")

if __name__ == '__main__':
    backfill()
