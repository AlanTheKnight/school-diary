from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    path('', views.TimeTableList.as_view(), name="list"),
]
