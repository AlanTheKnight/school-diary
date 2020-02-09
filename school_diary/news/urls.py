from django.urls import path
from . import views


urlpatterns = [
    path('page/<int:page>', views.get_posts),
    path('', views.first_page, name='news'),
    path('articles/<slug:url>', views.post),
    path('create/', views.create_post, name="news_create")
]
