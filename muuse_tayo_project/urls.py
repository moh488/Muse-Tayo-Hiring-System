from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from muuse_tayo_project.views import root_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='root'),
    path('dashboard/', include('dashboard.urls')),
    path('users/', include('users.urls')),
    path('jobs/', include('jobs.urls')),
    path('applicants/', include('applicants.urls')),
    path('selection/', include('selection.urls')),
    path('interviews/', include('interviews.urls')),
    path('messages/', include('messages.urls')),
    path('verifications/', include('verifications.urls')),
    path('reports/', include('reports.urls')),
    path('backups/', include('backups.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
