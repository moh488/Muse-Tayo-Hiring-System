from django.urls import path
from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics_dashboard'),
]
