from .forms import GetTimeTableForm
from django.shortcuts import render


def timetable(request):
    form = GetTimeTableForm()
    return render(request, 'timetable/timetable.html', {'form': form})
