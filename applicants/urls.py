from django.urls import path
from applicants import views

app_name = 'applicants'

urlpatterns = [
    path('', views.applicant_list, name='applicant_list'),
    path('add/', views.add_candidate, name='add_candidate'),
    path('mark-read/', views.mark_all_read, name='mark_all_read'),
    path('<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('<int:pk>/stage/', views.update_stage, name='update_stage'),
]
