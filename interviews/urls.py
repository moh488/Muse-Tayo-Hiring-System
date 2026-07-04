from django.urls import path
from interviews import views

app_name = 'interviews'

urlpatterns = [
    path('schedule/', views.schedule_interview, name='schedule_interview'),
    path('list/', views.interview_list, name='interview_list'),
]
