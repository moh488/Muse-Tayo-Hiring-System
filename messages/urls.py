from django.urls import path
from messages import views

app_name = 'messages'

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
]
