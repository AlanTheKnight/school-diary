from rest_framework import serializers
from timetable import models


class LessonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BellsTimeTable
        fields = ['n', 'start', 'end']


class LessonsSerializer(serializers.ModelSerializer):
    number = LessonNumberSerializer()

    class Meta:
        model = models.Lessons
        fields = ['number', 'subject', 'classroom']


class LessonsListSerializer(serializers.Serializer):
    weekday = serializers.CharField()
    lessons = LessonsSerializer(many=True)
