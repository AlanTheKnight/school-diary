from django.urls import path

from apps.api.diary import views

app_name = 'api_diary'

urlpatterns = [
    path('grades/', views.GradesList.as_view(), name="grades-list"),
    path('grades/<int:pk>', views.GradesDetails.as_view(), name="grade-details")
]
