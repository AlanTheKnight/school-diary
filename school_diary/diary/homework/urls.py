from django.urls import path
from . import views


urlpatterns = [
    path('homework/', views.show_homework, name="homework")
]
