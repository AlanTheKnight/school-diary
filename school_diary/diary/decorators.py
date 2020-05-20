from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[], message=""):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            context = {'message':message}
            return render(request, 'access_denied.html', context)
        return wrapper_func
    return decorator


def student_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 3:
            return view_func
        context = {'message':'Данная страница доступна только ученикам.'}
        return render(request, 'access_denied.html', context)
    return wrapper


def teacher_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 2:
            return view_func()
        context = {'message':"Данная страница доступна только учителям."}
        return render(request, 'access_denied.html', context)
    return wrapper
    

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.account_type == 1 or request.user.account_type == 0:
            return view_func(request, *args, **kwargs)
        return render(request, 'access_denied.html', {'message':"Данная страница доступна только администраторам."})
    return wrapper
