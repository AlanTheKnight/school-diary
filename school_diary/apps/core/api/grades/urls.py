from django.urls import path

from . import views

app_name = "grades"

urlpatterns = (
    path('table/', views.ListStudentGrades.as_view(), name='grades'),
    path('group', views.GetOrCreateGroupAPI.as_view(), name='get-group'),
    path('', views.Grade.as_view())
)
