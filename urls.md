# Website links map

## Single pages

App's name: *"pages"*  
Links prefix: no prefix

    '', views.homepage, name='homepage'
    'help/', views.get_help, name='help'
    'about/', views.about, name='about'
    'error/', views.error404, name='404'

## News

App's name: *"news"*  
Links prefix: "news/"

    'page/<int:page>', views.get_posts
    '', views.first_page, name='news'
    'articles/<slug:url>', views.post
    'create/', views.create_post, name="news_create"
    'dashboard/', views.dashboard_first, name='news_dashboard'
    'dashboard/<int:page>', views.dashboard
    'delete/<str:id>', views.news_delete, name="news_delete"
    'update/<str:id>', views.news_update, name="news_update")

## Minimums

App's name: *"minimum"*  
Links prefix: "minimum/"

    '', views.minimum, name='minimum'
    'dashboard/', views.dashboard_first_page, name='minimum_dashboard'
    'dashboard/<int:page>', views.dashboard
    'delete/<int:id>', views.delete, name='minimum_delete'
    'update/<int:id>', views.update, name='minimum_update'
    'create/', views.create, name='minimum_create')

## Diary (classes)

App's name: *"diary"*  
Links prefix: no prefix

    'add-student/', views.add_student_page, name="add_student_page"
    'add-student/<str:i>/', views.add_student, name="add_student"
    'add-grade/', views.create_grade_page, name='create_grade'
    'my-grade/', views.my_grade, name='my_grade'
    'delete-student/<str:i>', views.delete_student, name='delete_student'
    'students_marks/', views.view_students_marks, name='students_marks'
    'view_marks/<int:pk>/<int:term>', views.students_marks, name='view_marks'
    'mygradesettings', views.mygradesettings, name='grade-settings'

## Diary (marks)

App's name: *"diary"*  
Links prefix: no prefix

    'diary/lesson/<int:pk>', views.lesson_page, name='lesson-page'
    'diary/lesson/<int:pk>/delete', views.delete_lesson, name='diary_lesson_delete'
    'diary/', views.diary, name='diary'
    'diary/<int:id>/<int:term>/', views.stats, name='statistics'
    'diary/homework/', views.homework, name='homework'

## Admin dashboard

App's name: *"admin_panel"*  
Links prefix: no prefix  
TODO: Create a prefix for admin panel ("admin/")

### Students

    'students/', views.students_dashboard_first_page, name="students_dashboard"
    'students/<int:page>', views.students_dashboard, name="students_dashboard"
    'students/delete/<str:id>', views.students_delete, name='students_delete'
    'students/update/<str:id>', views.students_update, name='students_update'

### Teachers

    'teachers/', views.teachers_dashboard_first_page, name='teachers_dashboard'
    'teachers/<int:page>', views.teachers_dashboard, name='teachers_dashboard'
    'teachers/delete/<str:id>', views.teachers_delete, name='teachers_delete'
    'teachers/update/<str:id>', views.teachers_update, name='teachers_update'

### Administrators

    'admins/', views.admins_dashboard_first_page, name='admins_dashboard'
    'admins/<int:page>', views.admins_dashboard, name='admins_dashboard'
    'admins/delete/<str:id>', views.admins_delete, name='admins_delete'
    'admins/update/<str:id>', views.admins_update, name='admins_update'

### Messages

    'messages/', views.messages_dashboard_first_page, name='messages_dashboard'
    'messages/<int:page>', views.messages_dashboard, name='messages_dashboard'
    'messages/delete/<int:pk>', views.messages_delete, name='messages_delete'
    'messages/view/<int:pk>', views.messages_view, name='messages_view'

    'export/', views.export_page, name='export_marks'
    'export/<int:quarter>/', views.generate_table, name='export_marks_download'
    'empty-exported-folder/', views.empty_backup_folder, name="delete_all_sheets"

## Users & registration

App's name: *"accounts"*  
Links prefix: no prefix

    'register/', views.user_register, name='register'
    'login/', views.user_login, name='login'
    'logout/', views.user_logout, name='logout'
    'profile/', views.user_profile, name='profile'
    'admins/create', views.admin_register, name='admins_create'
    'teachers/create/', views.teacher_register, name='teachers_create'
    'new-message/', views.admin_message, name="message_to_admin"

## Password reset

App's name: *"accounts"*  
Links prefix: no prefix

    'reset_password/', name="reset_password"
    'reset_password_sent/', name="password_reset_done"
    'reset/<uidb64>/<token>/', name="password_reset_confirm"
    'reset_password_complete/', name="password_reset_complete"
