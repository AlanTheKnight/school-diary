from django.urls import path
from admin_panel.messages import views

urlpatterns = [
    path('messages/', views.messages_dashboard_first_page, name="messages_dashboard"),
    path('messages/<int:page>', views.messages_dashboard, name="messages_dashboard"),
    path('messages/delete/<int:pk>', views.messages_delete, name='messages_delete'),
    path('messages/view/<int:pk>', views.messages_view, name='messages_view'),
]
