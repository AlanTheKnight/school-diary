import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from diary.decorators import student_only
from diary import forms
from diary import homework


NO_GRADE_CONTEXT = {
    "message": ("Вы не состоите в классе. Попросите Вашего"
                "классного руководителя добавить Вас в класс.")
}


@login_required(login_url="login")
@student_only
def show_homework(request):
    """
    Page where students can see their homework.
    """
    student = request.user.student
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', NO_GRADE_CONTEXT)
    if "date" in request.GET:
        form = forms.DatePickForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data['date']
            lessons = homework.get_homework(grade, date)
            context = {'form': form, 'lessons': lessons, 'date': date}
            return render(request, 'homework/homework.html', context)
    start_date = datetime.date.today() + datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=7)
    lessons = homework.get_homework(grade, start_date, end_date)
    form = forms.DatePickForm()
    return render(request, 'homework/homework.html', {'form': form, 'lessons': lessons})
