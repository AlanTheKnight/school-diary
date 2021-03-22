from django.urls import path
from apps.admin_panel.bells import views

urlpatterns = [
    path('timetable/bells/create', views.bells_create, name='bells_create'),
    path('timetable/bells/', views.bells_dashboard_first_page, name='bells_dashboard'),
    path('timetable/bells/delete/<int:pk>', views.bells_delete, name='bells_delete'),
    path('timetable/bells/update/<int:pk>', views.bells_update, name='bells_update'),
    path('timetable/bells/<int:page>', views.bells_dashboard, name='bells_dashboard'),
    path('timetable/bells/table', views.bells_table),
    path('timetable/bells/aj_create_bell', views.bells_table_save),
]
