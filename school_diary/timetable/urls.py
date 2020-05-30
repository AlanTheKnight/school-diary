from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable, name='timetable'),
    path('<int:grade>/<str:litera>', views.output),
    path('download/', views.download, name='timetable_download')
]
