from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
    path("", views.main, name="users"),
    path("<int:page>", views.main, name="users"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("messages/<int:page>", views.messages, name="messages"),
    path("messages/", views.messages, name="messages"),
    path("message/<int:pk>", views.message, name="message")
]
