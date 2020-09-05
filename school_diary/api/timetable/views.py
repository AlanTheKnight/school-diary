from rest_framework import generics
from timetable import models
from api.timetable import serializers
import time
from django.shortcuts import get_object_or_404
from diary.models import Grades

DAYWEEK_NAMES = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье",
}


class TimeTableList(generics.ListAPIView):
    """
    Return a timetable for selected grade.
    """
    serializer_class = serializers.LessonsListSerializer

    def get_queryset(self):
        data = []
        class_number = self.kwargs['number']
        class_letter = self.kwargs['letter']
        CURRENT_DAY = time.localtime().tm_wday + 1
        current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
        if CURRENT_DAY != 6:
            next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
        my_grade = get_object_or_404(Grades, number=class_number, letter=class_letter)
        all_lessons = models.Lessons.objects.filter(connection=my_grade.id)
        data.extend([
            {
                "weekday": "today",
                "lessons": all_lessons.filter(day=current_day_name) if CURRENT_DAY != 7 else []
            },
            {
                "weekday": "tomorrow",
                "lessons": all_lessons.filter(day=next_day_name) if CURRENT_DAY != 6 else []
            }
        ])
        data.extend([
            {
                "weekday": weekday,
                "lessons": all_lessons.filter(day=weekday)
            } for weekday in DAYWEEK_NAMES.values() if weekday != "Воскресенье"
        ])
        return data
