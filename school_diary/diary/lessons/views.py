from django.shortcuts import render
from diary.forms import LessonCreationForm
import utils
from diary import utils as diary_utils


def lessons(request):
    subjects, grades = \
        diary_utils.default_grades_and_subjects(request.user.teacher)

    if not (grades and subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    form = LessonCreationForm()
    return render(request, "lessons.html", {'form': form})
