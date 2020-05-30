from django.urls import path
from admin_panel.teachers import views


urlpatterns = [
    path('', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('<int:page>', views.teachers_dashboard, name='teachers_dashboard'),
    path('delete/<str:id>', views.teachers_delete, name='teachers_delete'),
    path('update/<str:id>', views.teachers_update, name='teachers_update'),
]
