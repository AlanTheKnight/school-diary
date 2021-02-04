from django.shortcuts import render


def homepage(request):
    """
    Return a homepage.
    """
    return render(request, 'homepage.html')


def about(request):
    return render(request, 'about_us.html')
