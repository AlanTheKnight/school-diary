from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.dashboard_first_page, name='dashboard'),
    path('<int:page>/', views.dashboard, name='dashboard'),
    path('update/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
]
