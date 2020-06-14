from rest_framework import serializers
from timetable import models


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lessons
        fields = ['connection', 'day', 'number', 'subject', 'classroom']
        depth = 1
