from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.core.access import teacher_only, has_klass


@login_required(login_url="login")
@teacher_only
@has_klass
def my_klass(request):
    """
    Return page with information about teacher's klass.
    """
    klass = request.user.teacher.klass
    students = klass.students_set.all()
    context = {
        'klass': klass,
        'students': students,
    }
    return render(request, 'klasses/my_klass.html', context)
