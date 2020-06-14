from rest_framework import generics
# from rest_framework import filters as rf_filters
from timetable import models
from api import permissions
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
    permission_classes = [permissions.APIUserPermission]
    # filter_backends = [
    #     filters.BACKEND, rf_filters.OrderingFilter]
    # filterset_class = filters.PostSearchFilter
    serializer_class = serializers.LessonsSerializer

    def get_queryset(self):
        return models.Lessons.objects.all()
        CURRENT_DAY = time.localtime().tm_wday + 1
        # If current day isn't sunday, users will see timetable for today.
        current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
        # If current day isn't friday, users will see timetable for tomorrow.
        if CURRENT_DAY != 6:
            next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
        my_class = str(self.kwargs['number']) + self.kwargs['letter']
        my_grade = get_object_or_404(Grades, number=self.kwargs['number'], letter=self.kwargs['letter'])
        all_lessons = models.Lessons.objects.filter(connection=my_grade.id)
        # If current day is not Sunday, student may have lessons today.
        data["today"] = all_lessons.filter(day=current_day_name) if CURRENT_DAY != 7 else []
        # If current_day is not Saturday, student may have lessons on the next day.
        data["tomorrow"] = all_lessons.filter(day=next_day_name) if CURRENT_DAY != 6 else []
        for weekday in DAYWEEK_NAMES.values():
            data[weekday] = all_lessons.filter(day=weekday) 
