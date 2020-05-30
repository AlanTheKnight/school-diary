from django.urls import path
from . import views

urlpatterns = [
    path('', views.output, name='timetable'),
    path('ajax', views.aj),
    path('download/', views.download, name='timetable_download'),
]
