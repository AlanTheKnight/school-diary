from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('diary/lesson/<int:pk>', views.lesson_page, name='lesson-page'),
    path('diary/lesson/<int:pk>/delete', views.delete_lesson, name='diary_lesson_delete'),
    path('diary/', views.diary, name='diary'),
    path('diary/<int:pk>/<int:term>/', views.stats, name='statistics'),
    path('diary/visible-students/', views.visible_students, name="visible-students"),
    path('diary/', include('diary.homework.urls')),
    path('diary/lessons/', include('diary.lessons.urls')),
    path('diary/lesson_plan', views.lesson_plan, name="lesson-plan"),
    path('diary/lesson_plan/update/<int:id>', views.update_lesson_plan, name="update-lesson-plan"),
    path('diary/lesson_plan/delete/<int:id>', views.update_lesson_plan, name="delete-lesson-plan"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
