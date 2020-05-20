from django.urls import path
from . import views


urlpatterns = [
    path('students/', views.students_dashboard_first_page, name='students_dashboard'),
    path('students/dashboard/', views.students_dashboard_first_page, name='students_dashboard'),
    path('students/dashboard/<int:page>', views.students_dashboard),
    path('students/delete/<str:id>', views.students_delete, name='students_delete'),
    path('students/update/<str:id>', views.students_update, name='students_update'),

    path('teachers/', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('teachers/dashboard/', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('teachers/dashboard/<int:page>', views.teachers_dashboard),
    path('teachers/delete/<str:id>', views.teachers_delete, name='teachers_delete'),
    path('teachers/update/<str:id>', views.teachers_update, name='teachers_update'),

    path('admins/', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('admins/dashboard/', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('admins/dashboard/<int:page>', views.admins_dashboard),
    path('admins/delete/<str:id>', views.admins_delete, name='admins_delete'),
    path('admins/update/<str:id>', views.admins_update, name='admins_update'),

    path('messages/', views.messages_dashboard_first_page, name='messages_dashboard'),
    path('messages/dashboard/<int:page>', views.messages_dashboard),
    path('messages/delete/<int:pk>', views.messages_delete, name='messages_delete'),
    path('messages/view/<int:pk>', views.messages_view, name='messages_view'),
]
