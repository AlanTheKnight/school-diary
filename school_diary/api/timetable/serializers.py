from rest_framework import serializers
from timetable import models


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lessons
        fields = ['number', 'subject', 'classroom']


class LessonsListSerializer(serializers.Serializer):
    weekday = serializers.CharField()
    lessons = LessonsSerializer(many=True)
