from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import ProtectedError

from apps.core import models
from .forms import KlassCreationForm

PER_PAGE = 50


def main(request, page: int = 1):
    form = KlassCreationForm()
    if request.method == "POST":
        form = KlassCreationForm(request.POST)
        if form.is_valid():
            form.save()

    klasses = Paginator(models.Klasses.objects.all().order_by("number", "letter"), PER_PAGE).get_page(page)
    context = {
        "klasses": klasses,
        "form": form
    }
    return render(request, "admin_panel/klasses/../admin_panel/klasses/dashboard.html", context)


def edit(request, pk: int):
    klass = get_object_or_404(models.Klasses, pk=pk)
    form = KlassCreationForm(instance=klass)
    if request.method == "POST":
        if "delete" in request.POST:
            try:
                klass.delete()
            except ProtectedError:
                messages.error(request, "Не получается удалить класс, так как с ним связаны определенные данные.")
            return redirect('klasses:edit', pk=pk)
        form = KlassCreationForm(request.POST, instance=klass)
        if form.is_valid():
            form.save()
            return redirect('klasses:dashboard')

    context = {
        "klass": klass,
        "form": form
    }
    return render(request, "admin_panel/klasses/../admin_panel/klasses/edit.html", context)
