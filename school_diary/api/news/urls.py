from django.urls import path
from api.news import views

app_name = 'news_api'

urlpatterns = [
    path('', views.NewsList.as_view()),
    path('<slug:slug>', views.PostDetails.as_view()),
    path('create/', views.PostCreate.as_view()),
]
