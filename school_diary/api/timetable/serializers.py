from rest_framework import serializers
from timetable import models


class LessonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BellsTimeTable
        fields = ['n', 'start', 'end']


class LessonsSerializer(serializers.ModelSerializer):
    n = serializers.IntegerField(source="number.n")
    start = serializers.TimeField(source="number.start")
    end = serializers.TimeField(source="number.end")

    class Meta:
        model = models.Lessons
        fields = ['n', 'start', 'end', 'subject', 'classroom']


class LessonsListSerializer(serializers.Serializer):
    weekday = serializers.CharField()
    lessons = LessonsSerializer(many=True)
