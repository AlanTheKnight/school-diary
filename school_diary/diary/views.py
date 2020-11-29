from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .decorators import teacher_only, student_only
from . import models
from . import functions
from . import homework
import utils
import datetime

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
    if not utils.session_ok(request.session):
        return redirect('diary')
    data = utils.load_from_session(request.session, {'group': None, 'term': None})
    group = models.Groups.objects.get(id=data['group'])

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
    if not utils.session_ok(request.session):
        return redirect('diary')
    data = utils.load_from_session(request.session, {'group': None, 'term': None})
    group = models.Groups.objects.get(id=data['group'])
    term = data['term']

    lesson = models.Lessons.objects.get(pk=pk)
    if not utils.fool_teacher_protection(request.user.teacher, lesson):
        return render(request, 'access_denied.html', {
            'message': "Вы не можете удалить этот урок.",
        })

    form = forms.LessonCreationForm(instance=lesson)
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
    lesson = models.Lessons.objects.get(pk=pk)
    if not utils.fool_teacher_protection(request.user.teacher, lesson):
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
        all_marks = student.marks_set.filter(lesson__quarter=chosen_quarter, lesson__is_plan=False)
        if not all_marks:
            return render(request, 'no_marks.html')

        d = {}
        max_length, total_missed = 0, 0
        for group in groups:
            marks = all_marks.filter(
                lesson__group=group, lesson__is_plan=False).order_by("lesson__date")
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
    teacher = request.user.teacher
    available_subjects, available_grades \
        = utils.grades_and_subjects(teacher)

    # If teacher doesn't have available classes or subjects,
    # user is redirected to Access Denied page.
    if not (available_grades and available_subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    # If teacher has just chosen grade, subject & quarter, update these
    # values in current session.
    if request.method == 'POST' and 'getgrade' in request.POST:
        selectionForm = forms.GroupSelectionForm(request.POST)
        if selectionForm.is_valid():
            utils.load_into_session(
                request.session,
                {
                    'term': selectionForm.cleaned_data['quarters'],
                    'group': selectionForm.get_group().id
                }
            )
            # We got data from form, saved it into the session,
            # now we teacher is redirected back to this page.
        return redirect('diary')

    # Assume that teacher hasn't selected any class/subject yet.
    # If current session doesn't have values we need (group & quarter),
    # we load defaults.
    utils.set_default_session(
        request.session, available_subjects, available_grades)
    # Now we can redirect teacher back to diary page.
    # After the redirect, we will get all needed session data.

    # Finally, grade, subject & term chosen by teacher
    data = utils.load_from_session(request.session, {'group': None, 'term': None})
    group = models.Groups.objects.get(id=data['group'])
    quarter = data['term']

    # Initialising a form for selecting classes and subjects
    # and filling it with initial values (available subjects & classes)
    selectionForm = forms.GroupSelectionForm(
        classes=available_grades,
        subjects=available_subjects,
        initial={
            'classes': group.grade,
            'subjects': group.subject,
            'quarters': quarter
        }
    )

    if group.subject not in group.grade.subjects.all():
        return render(request, 'access_denied.html', {
            'message': "Предмет \"{}\" не изучается в {} классе".format(group.subject, group.grade)
        })

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
            hw_form.add_homework(group.id)

    context = {
        'form': form,
        'hw_form': hw_form,
        'group_form': selectionForm
    }

    functions.update_context(context, group, quarter)
    print(context)
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
    marks = student.marks_set.filter(lesson__group=group, lesson__quarter=term, lesson__is_plan=False)

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


@login_required(login_url="login")
@teacher_only
@transaction.atomic
def lesson_plan(request):
    teacher = request.user.teacher
    plan = models.Lessons.objects.filter(group__grade__teachers=teacher, is_plan=True)
    if request.method == 'POST':
        date = request.POST.get('date')
        theme = request.POST.get('theme')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')
        control = request.POST.get('control')

        if 'create' in request.POST:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            lesson = models.Lessons(date=date,
                                    quarter=utils.get_quarter_by_date(date),
                                    theme=theme,
                                    control=models.Controls.objects.get(pk=control),
                                    is_plan=True,
                                    group=utils.get_group(models.Subjects.objects.get(pk=subject),
                                                          models.Grades.objects.get(pk=grade))
                                    )
            lesson.save()
            redirect('lesson-plan')
        else:
            plan = plan.filter(date__icontains=date,
                               theme__icontains=theme,
                               group__subject__id__icontains=subject,
                               group__grade__id__icontains=grade,
                               control__id__icontains=control)

    context = {
        'lessons': plan,
        'grades': models.Grades.objects.filter(teachers=teacher),
        'subjects': models.Subjects.objects.filter(teachers=teacher),
        'controls': models.Controls.objects.all()
    }

    return render(request, 'lesson_plan.html', context)


@login_required(login_url="login")
@teacher_only
@transaction.atomic
def update_lesson_plan(request, id):
    if request.method == 'POST':
        date = request.POST.get('date')
        theme = request.POST.get('theme')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')
        control = request.POST.get('control')
        lesson = models.Lessons.objects.get(pk=id)
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        lesson.date = date
        lesson.theme = theme
        lesson.group = utils.get_group(models.Subjects.objects.get(pk=subject),
                                models.Grades.objects.get(pk=grade))
        lesson.control = models.Controls.objects.get(pk=control)
        lesson.quarter = utils.get_quarter_by_date(date)
        lesson.save()
        return redirect('lesson-plan')
    teacher = request.user.teacher
    context = {
        'plan': models.Lessons.objects.get(pk=id),
        'grades': models.Grades.objects.filter(teachers=teacher),
        'subjects': models.Subjects.objects.filter(teachers=teacher),
        'controls': models.Controls.objects.all()
    }
    return render(request, 'lesson_plan_update.html', context)


@login_required(login_url="login")
@teacher_only
@transaction.atomic
def update_lesson_plan(request, id):
    if request.method == 'POST':
        lesson = models.Lessons.objects.get(pk=id)
        lesson.delete()
        return redirect('lesson-plan')
    return render(request, 'delete_lesson_plan.html')
