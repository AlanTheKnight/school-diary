from rest_framework import serializers
from apps.timetable import models
from apps.core.api.serializers import SubjectSerializer


class LessonCreateSerializer(serializers.ModelSerializer):
    n = serializers.IntegerField(max_value=9, min_value=1)
    letter = serializers.CharField(max_length=1)
    number = serializers.IntegerField(min_value=1, max_value=11)
    subject = serializers.CharField(max_length=50, allow_blank=True)
    classroom = serializers.CharField(max_length=50, allow_blank=True)

    class Meta:
        model = models.Lessons
        fields = ['subject', 'classroom', 'n', 'letter', 'number', 'day']


class LessonsRequestSerializer(serializers.Serializer):
    number = serializers.IntegerField(required=False)
    letter = serializers.CharField(required=False)
    current = serializers.BooleanField(default=False)

    def validate(self, data):
        """
        Check that at least number & letter or current were specified.
        """
        if ('number' in data and 'letter' in data) or data.get('current'):
            raise serializers.ValidationError("Specify number & letter or mark current=True")
        return data


class LessonsSerializer(serializers.Serializer):
    class LessonsInnerSerializer(serializers.ModelSerializer):
        n = serializers.IntegerField(source="number.n")
        start = serializers.TimeField(source="number.start")
        end = serializers.TimeField(source="number.end")
        subject = SubjectSerializer()

        class Meta:
            model = models.Lessons
            fields = ['n', 'start', 'end', 'subject', 'classroom']

    weekday = serializers.IntegerField()
    lessons = LessonsInnerSerializer(many=True)


class LessonNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BellsTimeTable
        fields = ['n', 'start', 'end']
