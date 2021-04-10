from rest_framework import serializers
from apps.timetable import models



class LessonCreateSerializer(serializers.ModelSerializer):
    n = serializers.IntegerField(max_value=9, min_value=1)
    letter = serializers.CharField(max_length=1)
    number = serializers.IntegerField(min_value=1, max_value=11)
    subject = serializers.CharField(max_length=50, allow_blank=True)
    classroom = serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model = models.Lessons
        fields = ['subject', 'classroom', 'n', 'letter', 'number', 'day']
