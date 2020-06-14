from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('help/', views.get_help, name='help'),
    path('about/', views.about, name='about'),
    path('error/', views.error404, name='404'),
    path('get-involved/', views.help_us, name="help_us"),
]
