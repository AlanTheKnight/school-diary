from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from rest_framework import status

from .forms import GetMinimumForm, MinimumCreationForm
from .models import Documents
from .decorators import admin_only
from .serializer import ValidSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.parsers import JSONParser


def minimum(request):
    if request.method == 'POST':
        form = GetMinimumForm(request.POST)
        if form.is_valid():
            chosen_grade = form.cleaned_data['grade']
            chosen_subject = form.cleaned_data['subject']
            chosen_term = form.cleaned_data['term']
            try:
                minimum = Documents.objects.get(
                    grade=chosen_grade, term=chosen_term, subject=chosen_subject)
                return render(request, 'minimum_download.html', {'minimum': minimum})
            except:
                return render(request, 'error.html', {
                    'title': "Минимум не найден",
                    'error': "404",
                    'description': "Минимум, который Вы ищите, не найден."
                })
    else:
        form = GetMinimumForm()
    return render(request, 'minimum.html', {'form': form})


@api_view(['POST'])
def minimum_api(request):
    form = ValidSerializer(data=request.data)
    if form.is_valid():
        cleaned_data = request.data
        chosen_grade = request.data['grade']
        chosen_subject = request.data['subject']
        chosen_term = request.data['term']
        try:
            minimum = Documents.objects.filter(
                grade=chosen_grade, term=chosen_term, subject=chosen_subject)
            return Response(OrderedDict({'minimum': list(minimum.values())}), status=status.HTTP_200_OK)
        except:
            return Response(OrderedDict({
                'title': "Have Not File",
                'error': "404",
            }), status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(OrderedDict({
            'title': "Bad form",
            'error': "400",
        }), status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/login/')
@admin_only
def dashboard_first_page(request):
    return redirect('/minimum/dashboard/1')


@login_required(login_url='/login/')
@admin_only
def dashboard(request, page):
    minimums = Documents.objects.all()
    minumums = Paginator(minimums, 20)
    minimums = minumums.page(page)
    return render(request, 'minimum/dashboard.html', {'minimums': minimums})


@login_required(login_url='/login/')
@admin_only
def update(request, id):
    m = Documents.objects.get(id=id)
    if request.method == "POST":
        form = MinimumCreationForm(request.POST, request.FILES, instance=m)
        if form.is_valid():
            form.save()
            return redirect('/minimum/dashboard/1')
    form = MinimumCreationForm(instance=m)
    return render(request, 'minimum/update.html', {'form': form, })


@login_required(login_url='/login/')
@admin_only
def delete(request, id):
    m = Documents.objects.get(id=id)
    if request.method == "POST":
        m.delete()
        return redirect('/minimum/dashboard/1')
    return render(request, 'minimum/delete.html', {'m': m})


@login_required(login_url='/login/')
@admin_only
def create(request):
    if request.method == "POST":
        form = MinimumCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('minimum_dashboard')
    form = MinimumCreationForm()
    return render(request, 'minimum/create.html', {'form': form})
