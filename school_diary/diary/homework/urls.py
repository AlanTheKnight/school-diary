from django.urls import path
from . import views


urlpatterns = [
    path('homework/', views.homework, name="homework")
]
