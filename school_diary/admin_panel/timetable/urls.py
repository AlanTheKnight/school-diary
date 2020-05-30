from django.urls import path
from admin_panel.timetable import views


urlpatterns = [
    path('', views.tt_dashboard, name='timetable_dashboard'),
    path('update/<int:pk>', views.tt_lesson_update, name='timetable_update'),
    path('delete/<int:pk>', views.tt_lesson_delete, name='timetable_delete'),
    path('create/', views.tt_lesson_create, name="timetable_create"),
]
