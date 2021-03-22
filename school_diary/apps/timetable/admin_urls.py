from django.urls import path
from apps.timetable import admin_panel as views


urlpatterns = [
    path('', views.dashboard, name='timetable_dashboard'),
]
