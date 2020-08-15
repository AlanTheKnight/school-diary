from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable, name='timetable'),
    path('download/', views.download, name='timetable_download')
]
