import time
from collections import OrderedDict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Grades, Lessons
from .views import DAYWEEK_NAMES


@api_view(['GET'])
def output_api(request, grade, litera):
    data = {}
    """Shows the timetable depending on the url."""
    CURRENT_DAY = time.localtime().tm_wday + 1
    # If current day isn't sunday, users will see timetable for today.
    current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
    # If surrent day isn't friday, users will see timetable for tomorrow.
    if CURRENT_DAY != 6: next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
    try:
        class_number = int(grade)
        class_letter = litera
        my_class = str(class_number) + class_letter
        my_grade = Grades.objects.get(number=class_number, letter=class_letter)
        all_lessons = Lessons.objects.filter(connection=my_grade.id)
        if CURRENT_DAY != 7:
            data["today"] = list(all_lessons.filter(day=current_day_name).values())
        else:
            data["today"] = []
        if CURRENT_DAY != 6:
            data["tomorrow"] = list(all_lessons.filter(day=next_day_name).values())
        else:
            data["tomorrow"] = []
        for weekday in DAYWEEK_NAMES.values():
            data[weekday] = list(all_lessons.filter(day=weekday).values())
        print(data)
        return Response(OrderedDict({
            'current_weekday': current_day_name,
            'data': data,
            'my_grade': my_class
        }), status=status.HTTP_200_OK)
    except Exception as error:
        print(error)
        return Response(OrderedDict({
            'error': "404",
            'title': "Расписание не найдено"
        }), status=status.HTTP_418_IM_A_TEAPOT)