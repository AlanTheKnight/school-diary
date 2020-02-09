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
        'title': "Файл не найден.", 
        "description": "Мы не можем найти файл, который вы ищите."
        })
