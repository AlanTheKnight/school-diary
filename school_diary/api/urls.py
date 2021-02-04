from django.urls import path, include
from rest_framework.authtoken import views

app_name = "api"

urlpatterns = [
    path('news/', include('api.news.urls', namespace="news")),
    path('timetable/', include('timetable.api.urls', namespace="timetable")),
    path('auth/', views.obtain_auth_token),
    path('inbuilt/', include('core.api.urls', namespace='inbuilt')),
    path('', include('api.diary.urls', namespace='diary')),
]
