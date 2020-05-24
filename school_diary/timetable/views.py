from django.shortcuts import render, get_object_or_404
from urllib.parse import unquote
from .forms import GetTimeTableForm
from django.http import HttpResponseRedirect
from .models import Grades, Lessons
import time


DAYWEEK_NAMES = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}


def timetable(request):
    """Gets grade from form and redirects to the page showing its timetable."""
    if request.method == 'POST':
        form = GetTimeTableForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_litera = form.cleaned_data['litera']
            url = str(chosen_grade) + '/' + chosen_litera
            url = unquote(url)
            return HttpResponseRedirect(url)
    else:
        form = GetTimeTableForm()
        return render(request, 'timetable/timetable.html', {'form': form})


def output(request, grade, litera):
    data = {}
    """Shows the timetable depending on the url."""
    CURRENT_DAY = time.localtime().tm_wday + 1
    # If current day isn't sunday, users will see timetable for today.
    current_day_name = DAYWEEK_NAMES[CURRENT_DAY]
    # If surrent day isn't friday, users will see timetable for tomorrow.
    if CURRENT_DAY != 6:
        next_day_name = DAYWEEK_NAMES[(CURRENT_DAY + 1) % 7]
    class_number = int(grade)
    class_letter = litera
    my_class = str(class_number) + class_letter
    my_grade = get_object_or_404(Grades, number=class_number, letter=class_letter)
    all_lessons = Lessons.objects.filter(connection=my_grade.id)
    if CURRENT_DAY != 7:
        data["today"] = all_lessons.filter(day=current_day_name)
    else:
        data["today"] = []
    if CURRENT_DAY != 6:
        data["tomorrow"] = all_lessons.filter(day=next_day_name)
    else:
        data["tomorrow"] = []
    for weekday in DAYWEEK_NAMES.values():
        data[weekday] = all_lessons.filter(day=weekday)
    return render(request, 'timetable/list.html', {
        'current_weekday': current_day_name,
        'data': data,
        'my_grade': my_class})


def download(request):
    return render(request, 'timetable/download.html')
