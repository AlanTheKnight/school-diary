from django.urls import path, include

from . import views
from .validators import views as val_views

app_name = 'inbuilt'

urlpatterns = [
    path('save-mark', views.SaveMark.as_view(), name="save-mark"),
    path('add-comment', views.AddComment.as_view(), name="add-comment"),
    path('get-comment', views.GetCommentText.as_view(), name="get-comment"),
    path('controls/', views.ListControls.as_view(), name="list-controls"),
    path('quarter-valid', val_views.QuarterValidator.as_view(), name="quarter-valid"),
    path("lessons/", include("apps.core.api.lessons.urls", namespace="lessons")),
    path("grades/", include("apps.core.api.grades.urls", namespace="grades")),
    path("homework/", include("apps.core.api.homework.urls", namespace="homework")),
    path("users/", include("apps.core.api.users.urls", namespace="users"))
]
