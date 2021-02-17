from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin-extended/', admin.site.urls),
    path('timetable/', include('timetable.urls')),
    path('minimum/', include('minimum.urls')),
    path('admin/', include('admin_panel.urls')),
    path('', include('diary.urls')),
    path('', include('pages.urls')),
    path('', include('accounts.urls')),
    path('klasses/', include('klasses.urls', namespace="klasses")),
    path('news/', include('news.urls')),
    path('api/', include('api.urls', namespace="api")),
    path('', include('homework.urls')),
    path('notes/', include('notes.urls', namespace="notes"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
