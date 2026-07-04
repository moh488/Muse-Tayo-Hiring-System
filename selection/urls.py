from django.urls import path
from selection import views

app_name = 'selection'

urlpatterns = [
    path('', views.selected_candidates, name='selected_candidates'),
]
