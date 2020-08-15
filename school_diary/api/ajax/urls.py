from django.urls import path
from .views import *

app_name = 'ajax_api'

urlpatterns = [
    path('save_mark', SaveMark.as_view()),
]