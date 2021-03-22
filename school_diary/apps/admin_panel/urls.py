from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='admin_panel'),
    path('timetable/lessons/', include('apps.timetable.admin_urls')),
    path('timetable/bells/', include('apps.admin_panel.bells.urls')),
    path('export/', include('apps.admin_panel.export.urls')),
    path('klasses/', include('apps.admin_panel.klasses.urls', namespace='klasses')),
    path('upload/', include('apps.admin_panel.upload.urls', namespace="upload")),
    path('users/', include('apps.admin_panel.users.urls', namespace="users"))
]
