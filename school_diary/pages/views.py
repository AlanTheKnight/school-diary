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


def about(request):
    return render(request, 'about_us.html')
