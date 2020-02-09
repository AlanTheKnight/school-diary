from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('registeradmin', views.admin_register, name='admin_register'),
    path('registerteacher', views.teacher_register, name="teacher_register"),
    path('', views.diary, name='diary')
]
