from django.shortcuts import redirect, render


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.account_type == 1 or request.user.account_type == 0:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'access_denied.html', {'message':"Вы не администратор."})
    return wrapper_function