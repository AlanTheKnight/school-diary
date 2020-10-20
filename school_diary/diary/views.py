from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .decorators import teacher_only, student_only
from . import models
from . import functions
from . import homework
import utils


# Tuple of keys needed to be in request.session
# when teachers work with diary.
NEEDED_IN_SESSION = ('subject', 'grade', 'term')
# Context which is used when student doesn't belong to any grade.
NO_GRADE_CONTEXT = {
    "message": ("Вы не состоите в классе. Попросите Вашего"
                "классного руководителя добавить Вас в класс.")
}


@teacher_only
@login_required(login_url="/login/")
def visible_students(request):
    grade, subject, term = functions.get_session_data(
        request.session, models.Grades.objects.all(), models.Subjects.objects.all()
    )
    group = models.Groups.objects.get(subject=subject, grade=grade)
    form = forms.VisibleStudentsForm(instance=group)
    if request.method == "POST":
        form = forms.VisibleStudentsForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("diary")
    return render(request, "visible_students.html", context={"form": form})


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
    group = models.Groups.objects.get(subject=subject, grade=grade)
    form.fields["control"].queryset = functions.create_controls(group, term)
    if request.method == "POST":
        form = forms.LessonCreationForm(
            request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            deletefile = request.POST.get("deletefile") is not None
            form.save(group=group, deletefile=deletefile)
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
        groups = models.Groups.objects.filter(students=student, grade=grade)
        all_marks = student.marks_set.filter(lesson__quarter=chosen_quarter)
        if not all_marks:
            return render(request, 'no_marks.html')

        d = {}
        max_length, total_missed = 0, 0
        for group in groups:
            marks = all_marks.filter(
                lesson__group=group).order_by("lesson__date")
            if len(marks) > max_length:
                max_length = len(marks)
            data = functions.get_marks_data(marks)
            d[group] = [data[1], data[0], marks]
            total_missed += data[5]

        for group in d:
            d[group].append(range(max_length - len(d[group][2])))

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
    """
    Returns:
        If teacher doesn't have any grades or subjects available, return
        access denied page.
        Otherwise it returns "teacher.html" rendered page.
    """

    # Current teacher and it's available subjects & grades
    teacher = models.Teachers.objects.get(account=request.user)
    available_subjects = teacher.subjects.all().order_by('name')
    available_grades = models.Grades.objects.filter(
        teachers=teacher).order_by('number', 'letter')

    if not (available_grades and available_subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    # If teacher've just chosen grade, subject & quarter, update these
    # values in current session.
    if request.method == 'POST' and 'getgrade' in request.POST:
        subject = available_subjects.get(name=request.POST.get('subject'))
        grade = request.POST.get('grade')
        term = int(request.POST.get('term'))
        grade = available_grades.get(number=int(grade[0:-1]), letter=grade[-1])
        functions.load_to_session(
            request.session,
            term=term, subject=subject.id, grade=grade.id
        )
        return redirect('diary')

    if not functions.session_is_ok(request.session):
        current_quarter = functions.get_current_quarter()
        if not current_quarter:
            current_quarter = 1
        utils.load_into_session(request.session, {
            'subject': available_subjects[0].id,
            'grade': available_grades[0].id,
            'term': current_quarter,
        })

    # Finally, grade, subject & term chosen by teacher
    grade, subject, term = functions.get_session_data(
        request.session, grades=available_grades, subjects=available_subjects)

    if subject not in grade.subjects.all():
        return render(request, 'access_denied.html', {
            'message': "Предмет \"{}\" не изучается в {} классе".format(subject, grade)
        })

    # UPDATE: group retrieving
    group = models.Groups.objects.get_or_create(grade=grade, subject=subject)
    if group[1]:  # If it hasn't been created yet
        group[0].set_default_students()
    group = group[0]
    utils.load_into_session(request.session, {'group': group.id})

    # New lesson creation
    form = forms.LessonCreationForm()
    if request.method == "POST" and 'createlesson' in request.POST:
        form = forms.LessonCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(group=group)

    hw_form = forms.HomeworkForm()
    if request.method == "POST" and 'addhomework' in request.POST:
        hw_form = forms.HomeworkForm(request.POST, request.FILES)
        if hw_form.is_valid():
            homework.add_homework(hw_form.cleaned_data, group.id)

    context = {
        'teacher': teacher,
        'subjects': available_subjects,
        'grades': available_grades,
        'current_class': grade,
        'current_term': term,
        'current_subject': subject,
        'form': form,
        'hw_form': hw_form
    }
    functions.update_context(context, group, term)
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
    group = get_object_or_404(models.Groups, grade=grade, subject=subject)
    lessons = models.Lessons.objects.filter(group=group, quarter=term)
    marks = student.marks_set.filter(lesson__group=group, lesson__quarter=term)

    # If student has no marks than send him a page with info.
    # Otherwise, student will get a page with statistics and his results.
    if marks:
        sm_avg, avg, quantity, amounts, needed, missed = functions.get_marks_data(
            marks)

        data = []
        for i in range(5, 1, -1):
            data.append(amounts.count(i))
        data.append(missed)
        teachers = grade.teachers.filter(subjects=subject)
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
            'missed': missed,
            'teachers': teachers
        }
        return render(request, 'results.html', context)
    return render(request, 'no_marks.html')
