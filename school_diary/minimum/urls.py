from django.urls import path
from . import views


urlpatterns = [
    path('', views.minimum, name='minimum'),
    path('dashboard/', views.dashboard_first_page, name='minimum_dashboard'),
    path('dashboard/<int:page>', views.dashboard),
    path('delete/<int:id>', views.delete, name='minimum_delete'),
    path('update/<int:id>', views.update, name='minimum_update'),
    path('create/', views.create, name='minimum_create')
]
