from django.urls import path
from . import views

urlpatterns = [
    path('add-student/<str:i>/', views.add_student, name="add_student"),
    path('add-grade/', views.create_grade_page, name='create_grade'),
    path('my-grade/', views.my_grade, name='my_grade'),
    path('delete-student/<int:pk>', views.delete_student, name='delete_student'),
    path('view_marks/<int:student_id>/', views.students_marks, name='view_marks'),
    path('settings', views.settings, name='grade-settings'),
]
