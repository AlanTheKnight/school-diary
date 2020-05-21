from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Authorization and login
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('registerteacher', views.teacher_register, name="teacher_register"),

    # Students and grades
    path('add-student/', views.add_student_page, name="add_student_page"),
    path('add-student/<str:i>/', views.add_student, name="add_student"),
    path('add-grade/', views.create_grade_page, name='create_grade'),
    path('my-grade/', views.my_grade, name='my_grade'),
    path('delete-student/<str:i>', views.delete_student, name='delete_student'),
    path('students_marks/', views.view_students_marks, name='students_marks'),
    path('view_marks/<int:pk>/<int:term>', views.students_marks, name='view_marks'),
    path('mygradesettings', views.mygradesettings, name='grade-settings'),

    path('admins/create', views.admin_register, name='admins_create'),
    path('teachers/create/', views.teacher_register, name='teachers_create'),

    # Admin messages
    path('send-message-to-admin/', views.admin_message, name="message_to_admin"),

    # Reset password
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
        name="password_reset_complete"),

    # Main diary part
    path('diary/lesson/<int:pk>', views.lesson_page, name='lesson-page'),
    path('diary/lesson/<int:pk>/delete', views.delete_lesson, name='diary_lesson_delete'),
    path('diary/', views.diary, name='diary'),
    path('diary/<int:id>/<int:term>/', views.stats, name='statistics'),
    path('diary/homework/', views.homework, name='homework'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
