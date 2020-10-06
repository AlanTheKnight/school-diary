from django.urls import path
from . import views

app_name = 'inbuilt'

urlpatterns = [
    path('save-mark', views.SaveMark.as_view(), name="save-mark"),
    path('add-comment', views.AddComment.as_view(), name="add-comment"),
    path('get-comment', views.GetCommentText.as_view(), name="get-comment")
]
