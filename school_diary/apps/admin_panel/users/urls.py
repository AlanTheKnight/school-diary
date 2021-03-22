from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.main, name="users"),
    path("<int:page>", views.main, name="users"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("messages/<int:page>", views.admin_messages, name="messages"),
    path("messages/", views.admin_messages, name="messages"),
    path("message/<int:pk>", views.message_details, name="message"),
    path('message/delete/<int:pk>', views.message_delete, name="message-delete"),
    path('register-admin', views.register_admin, name='register_admin'),
    path('register-teacher', views.register_teacher, name='register_teacher'),
]
