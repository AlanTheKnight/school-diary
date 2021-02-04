from django.urls import path
from . import views


app_name = "lessons"


urlpatterns = (
    path('list-lessons', views.LessonsList.as_view(), name="lessons-list"),
    path('change-is-plan', views.ChangeLessonIsPlanned.as_view(), name="change-is-plan"),
    path('edit-lesson/<int:pk>', views.EditLesson.as_view(), name="edit-lesson"),
    path('delete-lesson/<int:pk>', views.DeleteLesson.as_view(), name="delete-lesson"),
    path('grades', views.ListStudentGrades.as_view(), name='grades'),
    path('get-group', views.GetOrCreateGroupAPI.as_view(), name='get-group'),
    path('<int:pk>', views.RetrieveLesson.as_view(), name='lesson-details')
)
