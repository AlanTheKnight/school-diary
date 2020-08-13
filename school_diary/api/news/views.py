from rest_framework import generics
from rest_framework import filters as rf_filters
from news import models
from api.news import serializers
from api.news import filters
from api import permissions


class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.APIUserPermission]
    lookup_field = 'slug'


class PostCreate(generics.CreateAPIView):
    serializer_class = serializers.PostSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.APIUserPermission]


class NewsList(generics.ListAPIView):
    serializer_class = serializers.NewsSerializer
    queryset = models.Publications.objects.all()
    permission_classes = [permissions.APIUserPermission]
    filter_backends = [
        filters.BACKEND, rf_filters.OrderingFilter]
    filterset_class = filters.PostSearchFilter
