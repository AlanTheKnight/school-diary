from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.ListUsersView.as_view(), name="user-list"),
    path('<int:pk>/', views.UserDetailView.as_view(), name="user-detail"),
    path('current', views.CurrentUserView.as_view(), name="current-user")
]
