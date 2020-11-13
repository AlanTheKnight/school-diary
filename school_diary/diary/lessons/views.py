from django.shortcuts import render
from diary.forms import LessonCreationForm
import utils


def lessons(request):
    subjects, grades = \
        utils.grades_and_subjects(request.user.teacher)

    if not (grades and subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    form = LessonCreationForm()
    return render(request, "lessons.html", {'form': form})
