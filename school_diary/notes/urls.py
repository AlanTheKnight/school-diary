from django.urls import path
from . import api
from . import views

app_name = 'notes'

urlpatterns = [
    path('api/categories/', api.ListCategories.as_view(), name='list-categories'),
    path('api/notes/', api.ListNotesGroups.as_view(), name='list-notes'),
    path('api/notes/<int:pk>', api.NoteGroupDetails.as_view(), name='notes-details'),
    path('api/my-notes', api.ListMyNotesGroups.as_view(), name='my-notes'),
    path('api/upload-notes', api.UploadNoteView.as_view(), name='upload-note'),
    path('api/delete-note/<int:pk>', api.DeleteNoteView.as_view(), name='delete-note'),
    path('', views.main, name="notes")
]
