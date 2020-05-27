from django.urls import path
from . import views


urlpatterns = [
    path('page/<int:page>', views.get_posts, name="news"),
    path('', views.first_page, name='news'),
    path('articles/<slug:url>', views.post, name="news_post_details"),
]
