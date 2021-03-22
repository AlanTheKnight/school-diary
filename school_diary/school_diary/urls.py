from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin-extended/', admin.site.urls),
    path('timetable/', include('apps.timetable.urls')),
    path('minimum/', include('apps.minimum.urls')),
    path('admin/', include('apps.admin_panel.urls')),
    path('', include('apps.diary.urls')),
    path('', include('apps.pages.urls')),
    path('', include('apps.accounts.urls')),
    path('klasses/', include('apps.klasses.urls', namespace="my_klass")),
    path('news/', include('apps.news.urls')),
    path('api/', include('apps.api.urls', namespace="api")),
    path('', include('apps.homework.urls')),
    path('notes/', include('apps.notes.urls', namespace="notes"))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
