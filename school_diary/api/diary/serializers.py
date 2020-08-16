from rest_framework import serializers
from diary import models


class GradeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grades
        exclude = ('teachers', 'subjects')


class GradeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grades
        fields = '__all__'
