from django.urls import path
from . import views

app_name = "klasses"

urlpatterns = [
    path("", views.main, name="dashboard"),
    path("<int:pk>/", views.edit, name="edit")
]
