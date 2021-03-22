from functools import wraps
from typing import Tuple

from django.shortcuts import redirect, render

MESSAGES = {
    'NO_GRADE': {
        'message': ("Вы не состоите в классе. Попросите Вашего"
                    "классного руководителя добавить Вас в класс.")
    },
    'NOT_SPECIAL': {
        'message': "Вы не староста класса."
    }
}


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_types: Tuple[int, ...]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.account_type in allowed_types:
                return view_func(request, *args, **kwargs)
            context = {
                'message': "Вам недоступна данная страница."
            }
            return render(request, 'access_denied.html', context)
        return wrapper_func
    return decorator


def student_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 3:
            return view_func(request, *args, **kwargs)
        context = {'message': 'Данная страница доступна только ученикам.'}
        return render(request, 'access_denied.html', context)
    return wrapper


def teacher_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 2:
            return view_func(request, *args, **kwargs)
        context = {'message': "Данная страница доступна только учителям."}
        return render(request, 'access_denied.html', context)
    return wrapper


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 1 or request.user.account_type == 0:
            return view_func(request, *args, **kwargs)
        context = {'message': "Данная страница доступна только администраторам."}
        return render(request, 'access_denied.html', context)
    return wrapper


def is_president(function):
    """Check `request.user.student` has a president status."""
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.student.president:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NOT_SPECIAL'])
    return wrapper


def in_klass(function):
    """Check `request.user.student` is in class."""
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.student.in_klass:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NO_GRADE'])
    return wrapper


def has_klass(function):
    """Check that `request.user` is a main teacher."""
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user.teacher, "klass"):
            return function(request, *args, **kwargs)
        return render(request, 'access_denied/teacher_no_class.html')
    return wrapper
