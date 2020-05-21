from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('minimum/', include('minimum.urls')),
    path('', include('admin_panel.urls')),
    path('', include('diary.urls')),
    path('', include('pages.urls')),
    path('news/', include('news.urls')),
]
