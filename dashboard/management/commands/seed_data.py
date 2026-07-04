from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from users.models import SystemUser
from jobs.models import JobRequisition
from applicants.models import Candidate, JobApplication
from interviews.models import InterviewSchedule
from messages.models import DirectMessage


class Command(BaseCommand):
    help = 'Seed sample data for Muuse Tayo Hiring System'

    def handle(self, *args, **options):
        if SystemUser.objects.filter(username='admin').exists():
            self.stdout.write('Seed data already exists. Skipping.')
            return

        admin = SystemUser.objects.create_user(
            username='admin', email='admin@muusetayo.com', password='admin123',
            role='ADMIN', is_verified=True, is_staff=True, is_superuser=True,
        )
        hr = SystemUser.objects.create_user(
            username='hr_manager', email='hr@muusetayo.com', password='hr123',
            role='HR_MANAGER', is_verified=True,
        )
        recruiter = SystemUser.objects.create_user(
            username='recruiter', email='recruiter@muusetayo.com', password='rec123',
            role='RECRUITER', is_verified=True,
        )
        interviewer = SystemUser.objects.create_user(
            username='interviewer', email='interviewer@muusetayo.com', password='int123',
            role='INTERVIEWER', is_verified=True,
        )

        job1 = JobRequisition.objects.create(
            title='Senior Civil Engineer',
            reference_code='MTHS-2026-1001',
            department='CIVIL',
            description='Lead civil engineering projects for commercial construction.',
            requirements='BSc Civil Engineering, 5+ years experience.',
            salary_range_min=5000, salary_range_max=8000,
            posted_by=hr, status='ACTIVE',
            deadline=timezone.now().date() + timedelta(days=60),
        )
        job2 = JobRequisition.objects.create(
            title='HSE Safety Officer',
            reference_code='MTHS-2026-1002',
            department='SAFETY',
            description='Ensure workplace safety compliance on construction sites.',
            requirements='HSE certification, site safety experience.',
            salary_range_min=3000, salary_range_max=5000,
            posted_by=recruiter, status='ACTIVE',
            deadline=timezone.now().date() + timedelta(days=45),
        )

        candidates_data = [
            ('Ahmed', 'Hassan', 'ahmed@email.com', 'APPLIED'),
            ('Fatima', 'Omar', 'fatima@email.com', 'SHORTLISTED'),
            ('Ibrahim', 'Yusuf', 'ibrahim@email.com', 'INTERVIEWING'),
            ('Amina', 'Ali', 'amina@email.com', 'SELECTED'),
            ('Mohamed', 'Farah', 'mohamed@email.com', 'HIRED'),
        ]
        for first, last, email, stage in candidates_data:
            cand = Candidate.objects.create(
                first_name=first, last_name=last, email=email,
                phone='+252612345678', experience_years=3,
                skills='AutoCAD, Project Management, Site Supervision',
            )
            JobApplication.objects.create(candidate=cand, job=job1, stage=stage)

        interview_app = JobApplication.objects.filter(stage='INTERVIEWING').first()
        if interview_app:
            iv = InterviewSchedule.objects.create(
                application=interview_app,
                title='Technical Review - Civil Engineer',
                interview_type='TECHNICAL',
                scheduled_time=timezone.now() + timedelta(hours=2),
                location_details='Conference Room A',
            )
            iv.interviewers.add(interviewer)

        DirectMessage.objects.create(
            sender=hr, recipient=recruiter,
            subject='New Applicant Review',
            body='Please review the shortlisted candidates for the Civil Engineer position.',
        )

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
        self.stdout.write('Login: admin / admin123 (ADMIN)')
        self.stdout.write('Login: hr_manager / hr123 (HR_MANAGER)')
        self.stdout.write('Login: recruiter / rec123 (RECRUITER)')
        self.stdout.write('Login: interviewer / int123 (INTERVIEWER)')
