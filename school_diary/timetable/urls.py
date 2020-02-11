from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable, name='timetable'),
    path('<int:grade>/<str:litera>', views.output),
    path('download/', views.download, name='timetable_download'),
    path('dashboard', views.dashboard, name='timetable_dashboard'),
    path('edit_lesson/<str:id>', views.edit_lesson, name='timetable_update'),
    path('delete_lesson/<str:id>', views.delete_lesson, name='timetable_delete'),
    path('create_lesson/', views.create_lesson, name="timetable_create")
]
