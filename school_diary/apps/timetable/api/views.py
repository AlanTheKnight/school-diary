import time

from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, serializers

from apps.timetable import models
from apps.core.api.serializers import SubjectSerializer


class TimeTableList(generics.ListAPIView):
    """
    Return a timetable for selected klass.
    """
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

    serializer_class = LessonsSerializer

    def get_queryset(self):
        class_number = self.kwargs['number']
        class_letter = self.kwargs['letter']
        current_day = time.localtime().tm_wday + 1
        next_day = (current_day + 1) % 7 if current_day != 6 else None
        my_klass = get_object_or_404(models.Klasses, number=class_number, letter=class_letter)
        all_lessons = models.Lessons.objects.filter(klass=my_klass.id)
        data = [
            {
                "weekday": weekday,
                "lessons": all_lessons.filter(day=weekday)
            } for weekday in range(1, 7)
        ]
        return data


class ListBells(generics.ListAPIView):
    class LessonNumberSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.BellsTimeTable
            fields = ['n', 'start', 'end']

    serializer_class = LessonNumberSerializer
    queryset = models.BellsTimeTable.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
