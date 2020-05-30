from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable, name='timetable'),
    path('<int:grade>/<str:litera>', views.output),
    path('download/', views.download, name='timetable_download'),
    path('dashboard', views.dashboard, name='timetable_dashboard'),
    path('edit_lesson/<str:id>', views.edit_lesson, name='timetable_update'),
    path('delete_lesson/<str:id>', views.delete_lesson, name='timetable_delete'),
    path('create_lesson/', views.create_lesson, name="timetable_create"),
    
    path('bells/create', views.bells_create, name='bells_create'),
    path('bells/', views.bells_dashboard_first_page, name='bells_dashboard'),
    path('bells/dashboard/', views.bells_dashboard_first_page, name='bells_dashboard'),
    path('bells/delete/<int:pk>', views.bells_delete, name='bells_delete'),
    path('bells/update/<int:pk>', views.bells_update, name='bells_update'),
    path('bells/dashboard/<int:page>', views.bells_dashboard),
    path('bells/table', views.bells_table),
    path('bells/aj_create_bell', views.bells_table_save),
]
