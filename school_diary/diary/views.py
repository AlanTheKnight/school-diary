from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, Http404
from core import forms, models
from core.access import teacher_only, student_only, in_klass
from . import functions
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
@transaction.atomic
def lesson_page(request, pk):
    """Page where teachers can edit lesson."""
    # If teacher haven't chosen grade, term and subject, redirect back to diary.
    if not utils.session_ok(request.session):
        return redirect('diary')
    data = utils.load_from_session(
        request.session, {'group': None, 'term': None})
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


def get_data(request):
    if "group_id" in request.COOKIES and "quarter" in request.COOKIES:
        group_id = int(request.COOKIES["group_id"])
        quarter = int(request.COOKIES["quarter"])
        try:
            group = models.Groups.objects.get(id=group_id)
            return group, quarter
        except models.Groups.DoesNotExist:
            pass
    return None


def get_teacher_page_data(request, subjects, klasses):
    group = models.Groups.create_group(
        klasses[0].id, subjects[0].id
    )
    quarter = models.Quarters.get_default_quarter().number

    if "group_id" in request.COOKIES and "quarter" in request.COOKIES:
        group_id = int(request.COOKIES["group_id"])
        quarter = int(request.COOKIES["quarter"])
        try:
            group = models.Groups.objects.get(id=group_id)
        except models.Groups.DoesNotExist:
            pass
    return group, quarter


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


@student_only
@in_klass
def students_diary(request):
    student: models.Students = request.user.student
    chosen_quarter = models.Quarters.get_default_quarter().number
    if 'quarter' in request.GET:
        chosen_quarter = int(request.GET.get('quarter'))
    form = forms.QuarterSelectionForm(initial={"quarter": chosen_quarter})
    response = student.get_grades(chosen_quarter)
    context = {
        'student': student,
        'term': chosen_quarter,
        'form': form,
    }
    if response is not None:
        context.update(response)
    return render(request, 'student/grades.html', context)


def teachers_diary(request):
    """
    Returns:
        If teacher doesn't have any grades or subjects available, return
        access denied page.
        Otherwise it returns "teacher.html" rendered page.
    """

    teacher = request.user.teacher
    available_subjects, available_klasses \
        = utils.grades_and_subjects(teacher)

    if not (available_klasses and available_subjects):
        return render(request, 'access_denied.html', {
            'message': "Пока что вы не указаны как учитель ни в одном классе."
        })

    group, quarter = get_teacher_page_data(
        request, available_subjects, available_klasses)

    selectionForm = forms.GroupSelectionForm(
        classes=available_klasses,
        subjects=available_subjects,
        initial={
            'classes': group.klass,
            'subjects': group.subject,
            'quarters': quarter
        }
    )

    if group.subject not in group.klass.subjects.all():
        return render(request, 'access_denied.html', {
            'message': "Предмет \"{}\" не изучается в {} классе".format(group.subject, group.klass)
        })

    form = forms.LessonCreationForm()
    if request.method == "POST" and 'createlesson' in request.POST:
        form = forms.LessonCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(group=group)
            form = forms.LessonCreationForm()

    hw_form = forms.HomeworkForm(prefix="homework")
    if request.method == "POST" and 'addhomework' in request.POST:
        hw_form = forms.HomeworkForm(request.POST, request.FILES, prefix="homework")
        if hw_form.is_valid():
            hw_form.add_homework(group)
            hw_form = forms.HomeworkForm(prefix="homework")

    lesson_edit_form = forms.LessonCreationForm(prefix="edit")
    if request.method == "POST" and "editLesson" in request.POST:
        lesson = models.Lessons.objects.get(pk=int(request.POST.get("id")))
        lesson_edit_form = forms.LessonCreationForm(request.POST, request.FILES, prefix="edit", instance=lesson)
        if lesson_edit_form.is_valid():
            lesson_edit_form.save(group=group)
            lesson_edit_form = forms.LessonCreationForm(prefix="edit")

    students_form = forms.VisibleStudentsForm(instance=group)
    if request.method == "POST" and 'visibleStudents' in request.POST:
        students_form = forms.VisibleStudentsForm(request.POST, instance=group)
        if students_form.is_valid():
            students_form.save()

    context = {
        'form': form,
        'hw_form': hw_form,
        'group_form': selectionForm,
        'visibleStudentsForm': students_form,
        'lessonEditForm': lesson_edit_form
    }

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
@in_klass
def stats(request, pk, quarter: int):
    """Return a page with results for one specified subject."""
    student: models.Students = request.user.student
    klass = student.klass
    subject = get_object_or_404(models.Subjects, pk=pk)
    if subject not in student.klass.subjects.all():
        return render(request, 'access_denied.html', {'message': "В вашем классе\
            не преподают запрашиваемый предмет."})
    try:
        group = models.Groups.objects.get(klass=klass, subject=subject)
    except models.Groups.DoesNotExist:
        raise Http404
    context = student.get_grades_by_group(quarter, group)

    # If student has no marks than send him a page with info.
    # Otherwise, student will get a page with statistics and his results.
    if context is not None:
        teachers = student.klass.teachers.filter(subjects=subject)
        context.update({
            "teachers": teachers,
            "quarter": quarter,
            "subject": subject
        })
        return render(request, 'student/results.html', context)
    return render(request, 'no_marks.html')

