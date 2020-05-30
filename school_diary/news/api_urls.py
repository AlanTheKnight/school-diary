from django.urls import path
from . import api_views


urlpatterns = [
    path('get_post', api_views.get_posts_api),
    path('post/<str:url>', api_views.post_api)
]