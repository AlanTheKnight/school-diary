from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.access import teacher_only, has_klass
from apps.core import models
from . import forms
from django.http import HttpResponseForbidden


@login_required(login_url="login")
@teacher_only
@has_klass
def add_student(request, pk: int):
    """
    Function defining the process of adding new student to a grade and confirming it.
    """
    me: models.Teachers = request.user.teacher
    s = models.Students.objects.get(account=pk)
    if s.klass is None:
        if request.method == "POST":
            me.klass.add_new_student(s)
            return redirect('klasses:my-klass')
        return render(request, 'klasses/klasses/add_student.html', {'s': s})
    context = {
        'message': "Вы пытаетесь добавить к себе в класс ученика, который уже состоит в классе."
    }
    return render(request, 'access_denied.html', context)


# @login_required(login_url="login")
# @teacher_only
# def create_grade_page(request):
#     if request.method == "POST":
#         form = forms.GradeCreationForm(request.POST)
#         if form.is_valid():
#             grade = form.save()
#             mt = models.Teachers.objects.get(account=request.user)
#             grade.main_teacher = mt
#             grade.save()
#             return redirect('my_grade')
#         context = {'form': form}
#         return render(request, 'grades/add_grade.html', context)
#     form = forms.GradeCreationForm()
#     context = {'form': form}
#     return render(request, 'grades/add_grade.html', context)


@login_required(login_url="login")
@teacher_only
@has_klass
def my_klass(request):
    """
    Page with information about teacher's klass.
    """
    klass = request.user.teacher.klass
    students = klass.students_set.all()
    form = forms.StudentSearchForm()
    context = {
        'form': form,
        'klass': klass,
        'students': students,
    }
    if "search" in request.GET:
        form = forms.StudentSearchForm(request.GET)
        search = form.get_students()
        context["search"] = search
    return render(request, 'klasses/klasses/my_klass.html', context)


# def students_marks(request, student_id):
#     teacher = request.user.teacher
#     if not hasattr(teacher, 'grade_curated') or teacher.grade_curated is None:
#         return render(request, 'grades/no_grade.html')
#     student = get_object_or_404(models.Students, pk=student_id)
#     if student.grade != teacher.grade_curated:
#         return render(request, 'access_denied.html', {
#             'message': 'Вы не можете просматривать оценки учеников из другого класса.'
#         })
#     term = request.GET.get('quarter')
#     if term is None:
#         current = functions.get_current_quarter()
#         term = current if current != 0 else 1
#     term = int(term)
#     groups = models.Groups.objects.filter(grade=student.grade, students=student)
#     all_marks = student.marks_set.filter(lesson__quarter=term)
#     if not all_marks:
#         return render(request, 'grades/marks.html', {'no_marks': True, 'term': term})

#     d = {}
#     max_length, total_missed = 0, 0
#     for group in groups:
#         marks = all_marks.filter(lesson__group=group, lesson__is_plan=False).order_by("lesson__date")
#         if len(marks) > max_length:
#             max_length = len(marks)
#         data = functions.get_marks_data(marks)
#         d[group] = [data[1], data[0], marks]
#         total_missed += data[5]

#     for group in d:
#         d[group].append(range(max_length - len(d[group][2])))

#     context = {
#         'student': student,
#         'd': d,
#         'max_length': max_length,
#         'total_missed': total_missed,
#         'term': term,
#     }
#     return render(request, 'grades/marks.html', context)


@login_required(login_url="login")
@teacher_only
@has_klass
def delete_student(request, pk: int):
    """
    Function defining the process of deleting a student from a grade and confirming it.

    Args:
        pk - primary key of student to be deleted.
    """
    me = request.user.teacher
    student = models.Users.objects.get(pk=pk).student
    if student.klass != me.klass:
        return HttpResponseForbidden("Вы пытаетесь удалить ученика из другого класса.")
    if request.method == "POST":
        student.klass = None
        # Prevent this student from displaying in the grade.
        groups = me.klass.groups_set.all()
        for group in groups:
            group.students.remove(student)
        student.save()
        return redirect('klasses:my-klass')
    return render(request, 'klasses/klasses/delete_student.html', {'s': student})


@login_required(login_url="login")
@teacher_only
@has_klass
def settings(request):
    me = request.user.teacher
    if request.method == "POST":
        form = forms.KlassSettingsForm(request.POST, instance=me.klass)
        if form.is_valid():
            form.save()
            return redirect('klasses:my-klass')
    form = forms.KlassSettingsForm(instance=me.klass)
    return render(request, 'klasses/klasses/settings.html', {'form': form})
