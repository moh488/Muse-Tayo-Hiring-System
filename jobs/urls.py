from django.urls import path
from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('post/', views.post_job, name='post_job'),
    path('list/', views.list_jobs, name='list_jobs'),
    path('job/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
]
