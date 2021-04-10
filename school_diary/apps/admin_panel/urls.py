from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='admin_panel'),
    path('timetable/', include('apps.timetable.admin_urls')),
    path('export/', include('apps.admin_panel.export.urls')),
    path('klasses/', include('apps.admin_panel.klasses.urls', namespace='klasses')),
    path('upload/', include('apps.admin_panel.upload.urls', namespace="upload")),
    path('users/', include('apps.admin_panel.users.urls', namespace="users"))
]
