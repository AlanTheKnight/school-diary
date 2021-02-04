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
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=None, message=""):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            context = {'message': message}
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
    def wrapper(request, *args, **kwargs):
        if request.user.student.president:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NOT_SPECIAL'])
    return wrapper


def in_klass(function):
    def wrapper(request, *args, **kwargs):
        if request.user.student.klass is not None:
            return function(request, *args, **kwargs)
        return render(request, 'access_denied.html', MESSAGES['NO_GRADE'])
    return wrapper


def has_klass(function):
    """Check that `request.user` is main teacher."""
    def wrapper(request, *args, **kwargs):
        if request.user.teacher.klass:
            return function(request, *args, **kwargs)
        return render('klasses/no_klass.html')
    return wrapper
