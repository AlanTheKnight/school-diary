from django.urls import path
from . import views

urlpatterns = [
    path('/<int:grade>/<str:litera>', views.output_api)
]