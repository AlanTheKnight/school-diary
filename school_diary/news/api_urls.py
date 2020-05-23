from django.urls import path
from . import views

urlpatterns = [
    path('get_post', views.get_posts_api),
    path('post/<str:url>', views.post_api)
]