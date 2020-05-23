from rest_framework import serializers
from . import models


class NewsSerializer(serializers.Serializer):
    class Meta:
        model = models.Publications
