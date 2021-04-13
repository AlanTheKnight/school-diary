from django.shortcuts import get_object_or_404
from rest_framework import generics, authentication, status
from rest_framework.response import Response

from . import serializers
from apps.timetable import models


class TimeTableList(generics.ListAPIView):
    """
    Return a timetable for selected klass
    """
    serializer_class = serializers.LessonsSerializer
    authentication_classes = [authentication.SessionAuthentication]

    def get(self, request, *args, **kwargs):
        serializer = serializers.LessonsRequestSerializer(data=request.data)
        if serializer.is_valid():
            return self.list(request, *args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        if self.request.GET.get("current") is not None \
                and not self.request.user.is_anonymous and \
                self.request.user.is_student and self.request.user.student.klass is not None:
            my_klass = self.request.user.student.klass
        else:
            class_number = self.request.GET.get('number')
            class_letter = self.request.GET.get('letter')
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
    serializer_class = serializers.LessonNumberSerializer
    queryset = models.BellsTimeTable.objects.all()
    authentication_classes = [authentication.SessionAuthentication]
