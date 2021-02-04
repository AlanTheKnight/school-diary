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


class LessonCreateSerializer(serializers.ModelSerializer):
    n = serializers.IntegerField(max_value=9, min_value=1)
    letter = serializers.CharField(max_length=1)
    number = serializers.IntegerField(min_value=1, max_value=11)
    subject = serializers.CharField(max_length=50, allow_blank=True)
    classroom = serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model = models.Lessons
        fields = ['subject', 'classroom', 'n', 'letter', 'number', 'day']
