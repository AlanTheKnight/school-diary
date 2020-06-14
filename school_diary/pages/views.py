from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


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
