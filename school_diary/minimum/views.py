from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GetMinimumForm
from .models import Documents


def minimum(request):
    if request.method == 'POST':
        form = GetMinimumForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_subject = form.cleaned_data['subject']
            chosen_term = form.cleaned_data['term']
            try:
                minimum = Documents.objects.get(grade=chosen_grade, term=chosen_term, subject=chosen_subject)
                return render(request, 'minimum_download.html', {'minimum': minimum})
            except:
                return render(request, 'error.html', {
                    'title': "Минимум не найден",
                    'error': "404",
                    'description': "Минимум, который вы ищите, не найден."
                })
    else:
        form = GetMinimumForm()
    return render(request, 'minimum.html', {'form': form})
