from django.urls import path
from apps.admin_panel.export import views

urlpatterns = [
    path('', views.export_page, name='export_marks'),
    path('<int:quarter>/', views.generate_table, name='export_marks_download'),
    path('empty-backup-folder/', views.empty_backup_folder, name="delete_all_sheets"),
]
