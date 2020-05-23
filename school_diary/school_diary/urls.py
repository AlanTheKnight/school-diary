from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin-extended/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('minimum/', include('minimum.urls')),
    path('admin/', include('admin_panel.urls')),
    path('', include('diary.urls')),
    path('', include('pages.urls')),
    path('', include('accounts.urls')),
    path('news/', include('news.urls')),
    path('api/timetable', include('timetable.api_urls')),
    path('api/news/', include('news.api_urls'))
]
