from django.urls import path

from . import views

app_name = "homework"

urlpatterns = [
    path('', views.ListHomeworkView.as_view(), name='list')
]
