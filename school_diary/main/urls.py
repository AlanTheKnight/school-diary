from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('social/', views.social, name='social'),
    path('help/', views.get_help, name='help'),
    path('error/', views.error404, name='404'),
    path('docs/', views.docs, name='docs'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)