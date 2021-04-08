from django.urls import path

from . import views

app_name = "lessons"

urlpatterns = (
    path('', views.LessonsList.as_view(), name="lessons-list"),
    path('<int:pk>', views.EditLesson.as_view(), name="edit-lesson"),
)
