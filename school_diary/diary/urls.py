from django.urls import path
from . import views

urlpatterns = [
    path('registration', views.students_registration, name='registration'),
    path('login', views.students_login, name='login')
]