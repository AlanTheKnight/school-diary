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

    # Students
    path('students/', views.students_dashboard_first_page, name='students_dashboard'),
    path('students/dashboard/', views.students_dashboard_first_page, name='students_dashboard'),
    path('students/dashboard/<int:page>', views.students_dashboard),
    path('students/delete/<str:id>', views.students_delete, name='students_delete'),
    path('students/update/<str:id>', views.students_update, name='students_update'),

    # Teachers
    path('teachers/create/', views.teacher_register, name='teachers_create'),
    path('teachers/', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('teachers/dashboard/', views.teachers_dashboard_first_page, name='teachers_dashboard'),
    path('teachers/dashboard/<int:page>', views.teachers_dashboard),
    path('teachers/delete/<str:id>', views.teachers_delete, name='teachers_delete'),
    path('teachers/update/<str:id>', views.teachers_update, name='teachers_update'),

    # Admins
    path('admins/create', views.admin_register, name='admins_create'),
    path('admins/', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('admins/dashboard/', views.admins_dashboard_first_page, name='admins_dashboard'),
    path('admins/dashboard/<int:page>', views.admins_dashboard),
    path('admins/delete/<str:id>', views.admins_delete, name='admins_delete'),
    path('admins/update/<str:id>', views.admins_update, name='admins_update'),

    # Messages
    path('messages/', views.messages_dashboard_first_page, name='messages_dashboard'),
    path('messages/dashboard/<int:page>', views.messages_dashboard),
    path('messages/delete/<int:pk>', views.messages_delete, name='messages_delete'),
    path('messages/view/<int:pk>', views.messages_view, name='messages_view'),

    # Admin messages
    path('send-message-to-admin/', views.admin_message, name="message_to_admin"),

    # Reset password
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset/reset.html",
                                                                 email_template_name='email/email_template.html'),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset/done.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/confirm.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset/complete.html"),
         name="password_reset_complete"),

    # Main diary part
    path('diary/lesson/<int:pk>', views.lesson_page, name='lesson-page'),
    path('diary/lesson/<int:pk>/delete', views.delete_lesson, name='diary_lesson_delete'),
    path('diary/', views.diary, name='diary'),
    path('diary/<int:id>/<int:term>/', views.stats, name='statistics'),
    path('diary/homework/', views.homework, name='homework'),

    # Main part of a website
    path('', views.homepage, name='homepage'),
    path('social/', views.social, name='social'),
    path('help/', views.get_help, name='help'),
    path('about/', views.about, name='about'),
    path('error/', views.error404, name='404'),

    path('export/', views.export_page, name='export'),
    path('export/<int:quarter>/', views.generate_table, name='download sheet'),
    path('empty-backup-folder/', views.empty_backup_folder),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))