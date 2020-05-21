from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Students and grades
    path('add-student/', views.add_student_page, name="add_student_page"),
    path('add-student/<str:i>/', views.add_student, name="add_student"),
    path('add-grade/', views.create_grade_page, name='create_grade'),
    path('my-grade/', views.my_grade, name='my_grade'),
    path('delete-student/<str:i>', views.delete_student, name='delete_student'),
    path('students_marks/', views.view_students_marks, name='students_marks'),
    path('view_marks/<int:pk>/<int:term>', views.students_marks, name='view_marks'),
    path('mygradesettings', views.mygradesettings, name='grade-settings'),

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
