from django.urls import path, include


urlpatterns = [
    path('news/', include('api.news.urls', namespace="api_news")),
]
