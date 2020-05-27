from django.urls import path
from . import views

urlpatterns = [
    path('add-student/', views.add_student_page, name="add_student_page"),
    path('add-student/<str:i>/', views.add_student, name="add_student"),
    path('add-grade/', views.create_grade_page, name='create_grade'),
    path('my-grade/', views.my_grade, name='my_grade'),
    path('delete-student/<str:i>', views.delete_student, name='delete_student'),
    path('students_marks/', views.view_students_marks, name='students_marks'),
    path('view_marks/<int:pk>/<int:term>', views.students_marks, name='view_marks'),
    path('mygradesettings', views.mygradesettings, name='grade-settings'),
]
