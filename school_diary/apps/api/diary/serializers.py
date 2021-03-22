from rest_framework import serializers
from apps.core import models


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Klasses
        exclude = ('teachers', 'subjects')


class GradeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Klasses
        fields = '__all__'
