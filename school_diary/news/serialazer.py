from rest_framework import serializers
from . import models


class ValidSerializer(serializers.Serializer):
    search_text = serializers.CharField()
