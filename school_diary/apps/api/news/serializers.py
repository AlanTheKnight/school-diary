from rest_framework import serializers

from apps.news import models


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publications
        fields = ['date', 'title', 'author', 'slug', 'image']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publications
        fields = ['date', 'title', 'author', 'content', 'slug', 'image']
