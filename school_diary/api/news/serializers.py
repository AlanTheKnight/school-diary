from rest_framework import serializers
from news import models


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Publications
        fields = ['date', 'title', 'author', 'content', 'slug', 'image']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Publications
        fields = ['id', 'date', 'title', 'author', 'content', 'slug', 'image']
