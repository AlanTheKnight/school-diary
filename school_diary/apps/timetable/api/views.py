from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication

from . import serializers, permissions
from apps.timetable import models


def get_timetable(klass: models.Klasses):
    all_lessons = models.Lessons.objects.filter(klass=klass.id)
    return [
        {
            "weekday": weekday,
            "lessons": all_lessons.filter(day=weekday)
        } for weekday in range(1, 7)
    ]


class TimeTableList(generics.ListAPIView):
    """
    Return timetable for selected class.
    """
    serializer_class = serializers.LessonsSerializer
    authentication_classes = [authentication.SessionAuthentication]

    def get_queryset(self):
        class_number = self.kwargs['number']
        class_letter = self.kwargs['letter']
        my_klass = get_object_or_404(models.Klasses, number=class_number, letter=class_letter)
        return get_timetable(my_klass)


class CurrentTimetableView(generics.ListAPIView):
    """
    Return timetable for ``request.user.student``.
    """
    serializer_class = serializers.LessonsSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.StudentInKlassPermission]

    def get_queryset(self):
        my_klass = self.request.user.student.klass
        return get_timetable(my_klass)


class ListBells(generics.ListAPIView):
    serializer_class = serializers.LessonNumberSerializer
    queryset = models.BellsTimeTable.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
