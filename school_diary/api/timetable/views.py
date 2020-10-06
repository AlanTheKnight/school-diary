from rest_framework import generics
from rest_framework import views
from timetable import models
from api.timetable import serializers
import time
from django.shortcuts import get_object_or_404
from . import utils
from rest_framework.response import Response


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
        my_grade = get_object_or_404(models.Grades, number=class_number, letter=class_letter)
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


class ListBells(generics.ListAPIView):
    serializer_class = serializers.LessonNumberSerializer
    queryset = models.BellsTimeTable.objects.all()


class CreateLesson(views.APIView):
    def post(self, request):
        serializer = serializers.LessonCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        num = serializer.validated_data['number']
        let = serializer.validated_data['letter']
        grade = models.Grades.objects.get_or_create(number=num, letter=let)[0]
        n = utils.generate_bell(serializer.validated_data['n'], num)
        response = {'created': bool(n[1])}
        n = n[0]

        subject = serializer.validated_data['subject']
        classroom = serializer.validated_data['classroom']

        try:
            lesson = models.Lessons.objects.get(
                number=n,
                connection=grade,
                day=serializer.validated_data['day']
            )
            if classroom or subject:
                lesson.subject = subject
                lesson.classroom = classroom
                lesson.save()
            else:
                lesson.delete()
        except models.Lessons.DoesNotExist:
            if not (classroom or subject):
                return Response(response, 200)
            models.Lessons.objects.create(
                number=n,
                subject=subject,
                classroom=classroom,
                connection=grade,
                day=serializer.validated_data['day']
            )

        return Response(response, 200)
