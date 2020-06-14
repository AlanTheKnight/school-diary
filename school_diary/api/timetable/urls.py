from django.urls import path
from api.timetable import views

app_name = 'api_timetable'

urlpatterns = [
    path('<int:number>/<str:letter>/', views.TimeTableList.as_view(), name="list"),
]
