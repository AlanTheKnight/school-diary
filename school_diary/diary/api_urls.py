from . import api_views
from django.urls import path

urlpatterns = [
    path('<int:term>', api_views.diary_api),
    path('student/<int:pk>', api_views.get_student),
    path('grade/<int:pk>', api_views.get_grade),
    path('lesson/<int:pk>', api_views.get_lesson),
    path('subject/<int:pk>', api_views.get_subject)
]