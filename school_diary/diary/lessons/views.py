from django.shortcuts import render, redirect
from diary.forms import LessonCreationForm
import utils
from diary import models


def lessons(request):
    if not utils.session_ok(request.session):
        return redirect('diary')
    data = utils.load_from_session(
        request.session, {'group': None, 'term': None})
    group = models.Groups.objects.get(id=data['group'])
    subjects, grades = \
        utils.grades_and_subjects(request.user.teacher)
    if not (grades and subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    form = LessonCreationForm()
    if request.method == "POST":
        form = LessonCreationForm(request.POST, request.FILES)
        if form.is_valid():
            deletefile = request.POST.get("deletefile") is not None
            form.save(group=group, deletefile=deletefile)
            return redirect('diary')
    return render(request, "lessons.html", {'form': form})
