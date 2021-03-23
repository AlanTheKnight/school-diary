from django.urls import path
from . import views

app_name = "my_klass"

urlpatterns = [
    path('my-klass/', views.my_klass, name='my-klass'),
]
