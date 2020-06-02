from news import models
from api.news import serializers
from rest_framework import generics
from rest_framework import permissions


class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'slug'


class PostCreate(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.IsAdminUser]


class NewsList(generics.ListAPIView):
    serializer_class = serializers.NewsSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.IsAdminUser]
