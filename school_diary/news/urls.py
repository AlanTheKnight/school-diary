from django.urls import path
from . import views


urlpatterns = [
    path('page/<int:page>', views.get_posts),
    path('', views.first_page, name='news'),
    path('articles/<slug:url>', views.post),
    path('create/', views.create_post, name="news_create"),
    path('dashboard/', views.dashboard_first, name='news_dashboard'),
    path('dashboard/<int:page>', views.dashboard),
    path('delete/<str:id>', views.news_delete, name="news_delete"),
    path('update/<str:id>', views.news_update, name="news_update")
]
