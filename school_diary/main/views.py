from django.contrib.auth.decorators import login_required
from django.shortcuts import render



def homepage(request):
    return render(request, 'homepage.html')



def social(request):
    return render(request, 'social.html')



def get_help(request):
    return render(request, 'help.html')


def error404(request):
    return render(request, 'error.html', {
        'error': "404", 
        'title': "Страница не найдена.", 
        "description": "Мы не можем найти страницу, которую вы ищите."
        })


def error500(request):
    return render(request, 'error.html', {
        'error': "500", 
        'title': "Что-то пошло не так", 
        "description": "Мы работаем над этим."
        })