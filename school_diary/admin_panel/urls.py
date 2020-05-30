from django.urls import path
from . import views


urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),

    path('students/', views.students_dashboard_first_page, name='students_dashboard'),
    path('students/<int:page>', views.students_dashboard, name='students_dashboard'),
    path('students/delete/<str:id>', views.students_delete, name='students_delete'),
    path('students/update/<str:id>', views.students_update, name='students_update'),

    path('teachers/', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('teachers/<int:page>', views.teachers_dashboard, name='teachers_dashboard'),
    path('teachers/delete/<str:id>', views.teachers_delete, name='teachers_delete'),
    path('teachers/update/<str:id>', views.teachers_update, name='teachers_update'),

    path('admins/', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('admins/<int:page>', views.admins_dashboard, name='admins_dashboard'),
    path('admins/delete/<str:id>', views.admins_delete, name='admins_delete'),
    path('admins/update/<str:id>', views.admins_update, name='admins_update'),

    path('messages/', views.messages_dashboard_first_page, name="messages_dashboard"),
    path('messages/<int:page>', views.messages_dashboard, name="messages_dashboard"),
    path('messages/delete/<int:pk>', views.messages_delete, name='messages_delete'),
    path('messages/view/<int:pk>', views.messages_view, name='messages_view'),

    path('export/', views.export_page, name='export_marks'),
    path('export/<int:quarter>/', views.generate_table, name='export_marks_download'),
    path('empty-backup-folder/', views.empty_backup_folder, name="delete_all_sheets"),

    path('news/create/', views.news_create, name="news_create"),
    path('news/', views.news_dashboard_first_page, name='news_dashboard'),
    path('news/<int:page>', views.news_dashboard, name='news_dashboard'),
    path('news/delete/<str:pk>', views.news_delete, name="news_delete"),
    path('news/update/<str:pk>', views.news_update, name="news_update"),

    path('timetable/lessons/', views.tt_dashboard, name='timetable_dashboard'),
    path(
        'timetable/lessons/update/<int:pk>', views.tt_lesson_update, name='timetable_update'),
    path(
        'timetable/lessons/delete/<int:pk>', views.tt_lesson_delete, name='timetable_delete'),
    path('timetable/lessons/create/', views.tt_lesson_create, name="timetable_create"),

    path('timetable/bells/create', views.bells_create, name='bells_create'),
    path('timetable/bells/', views.bells_dashboard_first_page, name='bells_dashboard'),
    path('timetable/bells/delete/<int:pk>', views.bells_delete, name='bells_delete'),
    path('timetable/bells/update/<int:pk>', views.bells_update, name='bells_update'),
    path('timetable/bells/<int:page>', views.bells_dashboard, name='bells_dashboard'),
]
