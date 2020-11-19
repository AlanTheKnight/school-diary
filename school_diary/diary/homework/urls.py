from django.urls import path
from . import views


urlpatterns = [
    path('homework/', views.show_homework, name="homework"),
    path('homework-list/', views.homework_list, name="homework-list"),
    path('homework-list/<int:quarter>', views.homework_list, name="homework-list"),
    path('homework-delete/<int:pk>', views.homework_delete, name="homework-delete"),
    path('homework-edit/<int:pk>', views.homework_edit, name="homework-edit"),
    path('homework-stats/', views.stats, name="homework-stats"),
    path('homework-stats/<int:quarter>', views.stats, name="homework-stats")
]
