from django.shortcuts import render
from diary import models


def homepage(request):
    """
    Return a homepage.

    Context:
        type - a type of user (None if anonymous)
        grade - shows which grade user belongs to if user is a student
    """
    context = {'type': (request.user.account_type if request.user.is_authenticated else None)}
    if context['type'] == 3:
        context.update({'grade': models.Students.objects.get(account=request.user).grade})
    return render(request, 'homepage.html', context)


def get_help(request):
    return render(request, 'docs.html')


def about(request):
    return render(request, 'about_us.html')


def help_us(request):
    return render(request, 'help_us.html')


def error404(request):
    return render(request, 'error.html', {
        'error': "404",
        'title': "Страница не найдена.",
        "description": "Мы не можем найти страницу, которую Вы ищите."
    })


def error500(request):
    return render(request, 'error.html', {
        'error': "500",
        'title': "Что-то пошло не так",
        "description": "Мы работаем над этим."
    })
