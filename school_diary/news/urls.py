from django.urls import path
from . import views


urlpatterns = [
    path('page/<int:page>', views.get_posts, name="news"),
    path('', views.first_page, name='news'),
    path('post/<slug:url>', views.post, name="news_post_details"),

    path('create/', views.news_create, name="news_create"),
    path('delete/<str:pk>', views.news_delete, name="news_delete"),
    path('update/<str:pk>', views.news_update, name="news_update"),
]
