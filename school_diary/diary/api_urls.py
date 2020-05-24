from . import api_views
from django.urls import path

urlpatterns = [
    path('', api_views.DiaryApi.as_view())
]