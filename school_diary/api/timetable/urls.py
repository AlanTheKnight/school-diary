from django.urls import path
from api.timetable import views

app_name = 'timetable'

urlpatterns = [
    path('<int:number>/<str:letter>/', views.TimeTableList.as_view(), name="list"),
    path('create/', views.CreateLesson.as_view(), name="create"),
]
