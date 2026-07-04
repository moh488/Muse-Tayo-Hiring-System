from django.urls import path
from users import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('pending/', views.pending_approval_view, name='pending_approval'),
    path('add/', views.add_user, name='add_user'),
    path('list/', views.user_list, name='user_list'),
]
