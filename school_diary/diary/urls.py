from django.urls import path
from . import views

urlpatterns = [
    path('diary/lesson/<int:pk>', views.lesson_page, name='lesson-page'),
    path('diary/lesson/<int:pk>/delete', views.delete_lesson, name='diary_lesson_delete'),
    path('diary/', views.diary, name='diary'),
    path('diary/<int:pk>/<int:quarter>/', views.stats, name='statistics'),
]
