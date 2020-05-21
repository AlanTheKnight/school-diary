from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('admins/create', views.admin_register, name='admins_create'),
    path('teachers/create/', views.teacher_register, name='teachers_create'),
    path('new-message/', views.admin_message, name="message_to_admin"),

    path(
        'reset_password/', auth_views.PasswordResetView.as_view(
            template_name="password_reset/reset.html",
            email_template_name='email/email_template.html'),
        name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="password_reset/done.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password_reset/confirm.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="password_reset/complete.html"),
        name="password_reset_complete")
]
