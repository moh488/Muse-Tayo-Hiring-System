from django.urls import path
from verifications import views

app_name = 'verifications'

urlpatterns = [
    path('', views.pending_approvals, name='pending_approvals'),
]
