from django.urls import path
from . import views
from .validators import views as val_views

app_name = 'inbuilt'

urlpatterns = [
    path('save-mark', views.SaveMark.as_view(), name="save-mark"),
    path('add-comment', views.AddComment.as_view(), name="add-comment"),
    path('get-comment', views.GetCommentText.as_view(), name="get-comment"),
    path('list-lessons', views.LessonsList.as_view(), name="list-lessons"),
    path('list-controls', views.ListControls.as_view(), name="list-controls"),
    path('quarter-valid', val_views.QuarterValidator.as_view(), name="quarter-valid")
]
