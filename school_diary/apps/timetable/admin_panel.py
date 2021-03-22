from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.access import admin_only
from apps.timetable import forms
from apps.timetable import models
from apps.timetable import utils


SCHOOLS = dict([
    (1, "Младшая школа"),
    (2, "Средняя и старшая школа"),
])


@login_required(login_url='/login/')
@admin_only
def dashboard(request):
    form = forms.GetTimeTableForm()
    if request.method == "POST":
        form = forms.GetTimeTableForm(request.POST)
        if form.is_valid():
            utils.load_into_session(request.session, form.cleaned_data)
        return redirect('timetable_dashboard')

    chosen = utils.load_from_session(request.session, {
        'grade': '1', 'litera': 'А'
    })

    form = forms.GetTimeTableForm(initial=chosen)
    my_klass = models.Klasses.objects.get_or_create(number=chosen['grade'], letter=chosen['litera'])[0]
    lessons = models.Lessons.objects.filter(klass=my_klass).order_by('day', 'number')
    context = {
        'form': form,
        'lessons': lessons,
        'number': chosen['grade'],
        'letter': chosen['litera'],
        'klass': my_klass,
    }
    return render(request, 'timetable/dashboard.html', context)
