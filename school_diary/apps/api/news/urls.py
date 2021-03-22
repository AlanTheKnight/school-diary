from django.urls import path
from apps.api.news import views

app_name = 'news_api'

urlpatterns = [
    path('', views.NewsList.as_view(), name="list"),
    path('create', views.PostCreate.as_view(), name="create"),
    path('details/<slug:slug>', views.PostDetails.as_view(), name="details"),
]
