from django.urls import path
from admin_panel.news import views

urlpatterns = [
    path('create/', views.news_create, name="news_create"),
    path('', views.news_dashboard_first_page, name='news_dashboard'),
    path('<int:page>', views.news_dashboard, name='news_dashboard'),
    path('delete/<str:pk>', views.news_delete, name="news_delete"),
    path('update/<str:pk>', views.news_update, name="news_update"),
]
