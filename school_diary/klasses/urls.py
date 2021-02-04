from django.urls import path
from . import views

app_name = "klasses"

urlpatterns = [
    path('add-student/<int:pk>/', views.add_student, name="add-student"),
    # path('add-grade/', views.create_grade_page, name='create_grade'),
    path('my-klass/', views.my_klass, name='my-klass'),
    path('delete-student/<int:pk>', views.delete_student, name='delete-student'),
    # path('view_marks/<int:student_id>/', views.students_marks, name='view_marks'),
    path('settings', views.settings, name='settings'),
]
