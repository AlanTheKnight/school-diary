from django.urls import path
from . import api_views


urlpatterns = [
    path('/<int:grade>/<str:litera>', api_views.output_api)
]