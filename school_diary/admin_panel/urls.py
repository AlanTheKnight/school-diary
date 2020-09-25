from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='admin_panel'),

    path('admins/', include('admin_panel.admins.urls')),
    path('students/', include('admin_panel.students.urls')),
    path('teachers/', include('admin_panel.teachers.urls')),
    path('timetable/lessons/', include('admin_panel.timetable.urls')),
    path('timetable/bells/', include('admin_panel.bells.urls')),
    path('messages/', include('admin_panel.messages.urls')),
    path('export/', include('admin_panel.export.urls')),
    path('grades/', include('admin_panel.grades.urls', namespace='grades')),
]
