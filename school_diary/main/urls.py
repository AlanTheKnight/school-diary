from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('social/', views.social, name='social'),
    path('help/', views.get_help, name='help'),
    path('error/', views.error404, name='404'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.error404
handler500 = views.error500