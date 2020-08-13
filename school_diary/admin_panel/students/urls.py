from django.urls import path
from admin_panel.students import views

urlpatterns = [
    path('', views.students_dashboard_first_page, name='students_dashboard'),
    path('<int:page>', views.students_dashboard, name='students_dashboard'),
    path('delete/<str:id>', views.students_delete, name='students_delete'),
    path('update/<str:id>', views.students_update, name='students_update'),
]
