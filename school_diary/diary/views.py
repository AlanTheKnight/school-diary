import datetime
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .decorators import teacher_only, student_only
from . import models
from . import functions


# Tuple of keys needed to be in request.session
# when teachers work with diary.
NEEDED_IN_SESSION = ('grade', 'subject', 'term')
# Context which is used when student doesn't belong to any grade.
NO_GRADE_CONTEXT = {
    "message": ("Вы не состоите в классе. Попросите Вашего"
                "классного руководителя добавить Вас в класс.")
}


@teacher_only
@login_required(login_url="/login/")
@transaction.atomic
def lesson_page(request, pk):
    """Page where teachers can edit lesson."""
    # If teacher haven't chosen grade, term and subject, redirect back to diary.
    if not functions.each_contains(request.session, NEEDED_IN_SESSION):
        return redirect('diary')
    lesson = models.Lessons.objects.get(pk=pk)
    if not functions.fool_teacher_protection(request.user.id, lesson):
        return render(request, 'access_denied.html', {
            'message': "Вы не можете удалить этот урок.",
        })
    form = forms.LessonCreationForm(instance=lesson)
    grade, subject, term = functions.get_session_data(request.session)
    form.fields["control"].queryset = functions.create_controls(grade, subject, term)
    if request.method == "POST":
        form = forms.LessonCreationForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            deletefile = request.POST.get("deletefile") is not None
            form.save(subject=subject, grade=grade, deletefile=deletefile)
            return redirect('diary')
    context = {'form': form, 'lesson': lesson}
    return render(request, 'lesson_page.html', context)


@login_required(login_url='/login/')
@teacher_only
def delete_lesson(request, pk):
    """
    Asks teacher's confirmation and then deletes the selected lesson.
    """
    if not functions.each_contains(request.session, NEEDED_IN_SESSION):
        return redirect('diary')
    lesson = models.Lessons.objects.get(pk=pk)
    # Fool protection for users who will try to delete a lesson of another teacher.
    if not functions.fool_teacher_protection(request.user.id, lesson):
        return render(request, 'access_denied.html', {
            'message': "Вы не можете удалить этот урок.",
        })
    if request.method == "POST":
        lesson.delete()
        return redirect('diary')
    return render(request, 'lesson_delete.html', {'item': lesson})


def students_diary(request):
    student = request.user.student
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', {'message': "Вы не состоите в классе.\
        Попросите Вашего классного руководителя добавить Вас в класс."})
    if request.method == "POST" and 'all' in request.POST:
        chosen_quarter = int(request.POST.get('term'))
        subjects = grade.subjects.all()
        all_marks = student.marks_set.filter(lesson__quarter=chosen_quarter)
        if not all_marks:
            return render(request, 'no_marks.html')
        d = {}
        max_length, total_missed = 0, 0
        for s in subjects:
            marks = all_marks.filter(subject=s.id).order_by('lesson__date')
            if len(marks) > max_length:
                max_length = len(marks)
            data = functions.get_marks_data(marks)
            d[s] = [data[1], data[0], marks]
            total_missed += data[5]
        for subject in d:
            d[subject].append(range(max_length - len(d[subject][2])))
        context = {
            'student': student,
            'd': d,
            'max_length': max_length,
            'total_missed': total_missed,
            'term': chosen_quarter,
        }
        return render(request, 'marklist.html', context)
    return render(request, 'diary_student.html')


def teachers_diary(request):
    teacher = models.Teachers.objects.get(account=request.user)  # Current teacher
    available_classes = models.Grades.objects.filter(teachers=teacher).order_by('number', 'letter')
    available_subjects = teacher.subjects.all().order_by('name')
    if not (available_classes and available_subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })
    if request.method == 'POST' and 'getgrade' in request.POST:
        subject = available_subjects.get(name=request.POST.get('subject'))
        grade = request.POST.get('grade')
        term = int(request.POST.get('term'))
        grade = available_classes.get(number=int(grade[0:-1]), subjects=subject, letter=grade[-1])
        functions.load_to_session(
            request.session,
            term=term, subject=subject.id, grade=grade.id
        )
        return redirect('diary')
    if not functions.each_contains(request.session, NEEDED_IN_SESSION):
        current_quarter = functions.get_current_quarter()
        if not current_quarter:
            current_quarter = 1
        request.session['subject'] = available_subjects[0].id  # Loading default data into session
        request.session['grade'] = available_classes[0].id
        request.session['term'] = current_quarter
    # Creating table with marks and setting up available controls.
    grade_, subject_, term_ = functions.get_session_data(
        request.session, grades=available_classes, subjects=available_subjects)
    form = forms.LessonCreationForm()
    if request.method == "POST" and 'createlesson' in request.POST:
        form = forms.LessonCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(subject=subject_, grade=grade_)
    context = {
        'TEACHER': teacher, 'subjects': available_subjects,
        'grades': available_classes, 'current_class': grade_,
        'current_term': term_, 'current_subject': subject_,
        'form': form
    }
    if request.method == "POST":
        if 'addcomment' in request.POST:
            functions.add_comment_to_mark(request.POST)
        else:
            functions.save_marks(request.POST, grade_, subject_)
    functions.update_context(context, grade_, term_, subject_)
    return render(request, 'teacher.html', context)


@login_required(login_url="/login/")
def diary(request):
    """
    Main function for displaying diary pages to admins/teachers/students.
    """
    if 0 <= request.user.account_type <= 1:
        return redirect('admin_panel')
    elif request.user.account_type == 3:
        return students_diary(request)
    elif request.user.account_type == 2:
        return teachers_diary(request)
    return redirect('homepage')


@login_required(login_url="login")
@student_only
def stats(request, pk, term):
    """Return a page with results for one specified subject."""
    student = request.user.student
    grade = student.grade
    if grade is None:
        return render(request, 'access_denied.html', {'message': "Вы не состоите в классе.\
            Попросите Вашего классного руководителя добавить Вас в класс."})
    subject = get_object_or_404(models.Subjects, pk=pk)
    if subject not in student.grade.subjects.all():
        return render(request, 'access_denied.html', {'message': "В вашем классе\
            не преподают запрашиваемый предмет."})
    lessons = models.Lessons.objects.filter(grade=grade, subject=subject, quarter=term)
    marks = student.marks_set.filter(subject=subject, lesson__quarter=term)

    # If student has no marks than send him a page with info.
    # Otherwise, student will get a page with statistics and his results.
    if marks:
        sm_avg, avg, quantity, amounts, needed, missed = functions.get_marks_data(marks)

        data = []
        for i in range(5, 1, -1):
            data.append(amounts.count(i))
        data.append(missed)
        context = {
            'term': term,
            'lessons': lessons,
            'marks': marks,
            'subject': subject,
            'data': data,
            'avg': avg,
            'smartavg': sm_avg,
            'quantity': quantity,
            'needed': needed,
            'missed': missed
        }

        return render(request, 'results.html', context)
    return render(request, 'no_marks.html')


@login_required(login_url="login")
@student_only
def homework(request):
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
            lessons = functions.get_homework(grade, date)
            context = {'form': form, 'lessons': lessons, 'date': date}
            return render(request, 'homework.html', context)
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=6)
    lessons = functions.get_homework(grade, start_date, end_date)
    form = forms.DatePickForm()
    return render(request, 'homework.html', {'form': form, 'lessons': lessons})
