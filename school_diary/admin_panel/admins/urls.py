from django.urls import path
from admin_panel.admins import views

urlpatterns = [
    path('', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('<int:page>', views.admins_dashboard, name='admins_dashboard'),
    path('delete/<str:id>', views.admins_delete, name='admins_delete'),
    path('update/<str:id>', views.admins_update, name='admins_update'),
]
