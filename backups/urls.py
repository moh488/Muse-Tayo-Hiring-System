from django.urls import path
from backups import views

app_name = 'backups'

urlpatterns = [
    path('', views.export_panel, name='export_panel'),
]
