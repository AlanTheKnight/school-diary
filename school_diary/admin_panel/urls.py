from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='admin_panel'),
    path('timetable/lessons/', include('timetable.admin_urls')),
    path('timetable/bells/', include('admin_panel.bells.urls')),
    path('export/', include('admin_panel.export.urls')),
    path('grades/', include('admin_panel.grades.urls', namespace='grades')),
    path('upload/', include('admin_panel.upload.urls', namespace="upload")),
    path('users/', include('admin_panel.users.urls', namespace="users"))
]
